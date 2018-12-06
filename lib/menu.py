import curses
from curses import panel
from types import LambdaType

class BaseMenu:
    def __init__(self, stdscreen):
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

    def up(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        
    def down(self):
        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def update(self):
        self.window.refresh()
        curses.doupdate()

class Menu(BaseMenu):
    def __init__(self, stdscreen, title, items):
        super().__init__(stdscreen)
        self.should_exit = False
        self.position = 0
        self.title = title
        self.items = items
        self.items.append(('Exit', self.exit))

    def exit(self):
        self.should_exit = True

    def navigate(self, offset):
        self.position += offset
        self.position %= len(self.items)

    def draw_title(self):
        self.window.addstr(1, 1, self.title, curses.A_BOLD)

    def draw(self):
        self.draw_title()
        for index, item in enumerate(self.items):
            text = '%d. %s' % (index + 1, item[0])
            text_mode = curses.A_REVERSE if index == self.position else curses.A_NORMAL
            self.window.addstr(index + 3, 1, text, text_mode)

    def select(self, index):
        self.items[index][1]()
            
    def input(self, key):
        # ESC to quit
        if key == 27:
            self.window.nodelay(True)
            key = self.window.getch()
            if key == -1:
                return self.exit()

        # q to quit
        if key == ord('q'):
            return self.exit()

        # Enter to select item
        if key in [curses.KEY_ENTER, ord('\n')]:
            self.select(self.position)

        # Number keys to select item
        if key - ord('0') in range(1, len(self.items) + 1):
            self.select(key - ord('0') - 1)

        # Arrow keys or jk to navigate
        if key in [curses.KEY_UP, ord('k')]:
            self.navigate(-1)

        elif key in [curses.KEY_DOWN, ord('j')]:
            self.navigate(1)

    def display(self):
        self.up()
        while not self.should_exit:
            self.update()
            self.draw()
            key = self.window.getch()
            self.input(key)

        self.should_exit = False
        self.down()

class ChecklistMenu(Menu):
    def __init__(self, stdscreen, title, items, default):
        super().__init__(stdscreen, title, items)
        self.states = [default] * len(items)
    
    def draw(self):
        self.draw_title()
        for index, item in enumerate(self.items):
            text = ''
            if isinstance(item[1], LambdaType):
                text = '%d. [ %s ] %s' % (index + 1, '*' if self.states[index] else ' ', item[0])
            else:
                text = '%d. %s' % (index + 1, item[0])

            text_mode = curses.A_REVERSE if index == self.position else curses.A_NORMAL
            self.window.addstr(index + 3, 1, text, text_mode)

    def input(self, key):
        super().input(key)

        if key == ord('\t'):
            self.expand(self.position)

    def expand(self, index):
        if len(self.items[index]) >= 3:
            self.items[index][2]()

    def select(self, index):
        self.states[index] = not self.states[index]
        fn = self.items[index][1]
        if isinstance(fn, LambdaType):
            fn(self.states[index])
        else:
            fn()

