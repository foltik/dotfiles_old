#!/usr/bin/python

import curses
from curses import panel

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
    def __init__(self, stdscreen, items):
        super().__init__(stdscreen)
        self.should_exit = False
        self.position = 0
        self.items = items
        self.items.append(('exit', self.exit))

    def exit(self):
        self.should_exit = True

    def navigate(self, offset):
        self.position += offset
        self.position %= len(self.items)

    def draw(self):
        for index, item in enumerate(self.items):
            text = '%d. %s' % (index + 1, item[0])
            text_mode = curses.A_REVERSE if index == self.position else curses.A_NORMAL
            self.window.addstr(index + 1, 1, text, text_mode)

    def get_selection(self, key):
        if key in [curses.KEY_ENTER, ord('\n')]:
            return self.items[self.position]
        elif (key - ord('0')) in range(1, len(self.items) + 1):
            return self.items[key - ord('0') - 1]
        else:
            return None

    def input(self):
        key = self.window.getch()
        selection = self.get_selection(key)

        if selection:
            selection[1]()

        if key == curses.KEY_UP:
            self.navigate(-1)
        elif key == curses.KEY_DOWN:
            self.navigate(1)

    def display(self):
        self.up()
        while not self.should_exit:
            self.update()
            self.draw()
            self.input()

        self.should_exit = False
        self.down()
    
class App(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        submenu_items = [
            ('beep', curses.beep),
            ('flash', curses.flash)
        ]
        submenu = Menu(self.screen, submenu_items)

        main_menu_items = [
            ('beep', curses.beep),
            ('flash', curses.flash),
            ('submenu', submenu.display)
        ]
        main_menu = Menu(self.screen, main_menu_items)
        main_menu.display()

if __name__ == '__main__':
    curses.wrapper(App)

        
