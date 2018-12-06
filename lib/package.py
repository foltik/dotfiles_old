from pathlib import Path
from lib.menu import ChecklistMenu

def toggle(obj, prop):
    return lambda b: setattr(obj, prop, b)

class Package:
    def __init__(self, obj):
        # Immutable Attributes
        if isinstance(obj, dict):
            self.name, props = next(iter(obj.items()))
            self.source = 'core'
            for key, value in props.items():
                setattr(self, key, value)
        else:
            self.name = obj
            self.source = 'core'
        self.update_from_files()

        # Install State
        self.enabled = True
        self.install = True
        self.copy_config = True
        self.run_script = True
        self.enable_units = True

        
    def __repr__(self):
        return self.name

    def update_from_files(self):
        if self.source == 'none':
            self.source = None
        
        default_config = Path('lain/.config/' + self.name)
        if hasattr(self, 'config'):
            self.config = Path('lain/' + self.config)
        elif default_config.is_dir():
            self.config = default_config
        else:
            self.config = None
        
        default_script = Path('scripts/' + self.name + '.fish')
        if hasattr(self, 'script'):
            self.script = Path('scripts/' + self.script)
        elif default_script.is_file():
            self.script = default_script
        else:
            self.script = None

        default_unit = Path('lain/.config/systemd/user/' + self.name + '.service')
        if hasattr(self, 'userunits'):
            self.userunits = list(map(lambda unit: Path('lain/.config/systemd/user/' + unit), self.userunits))
        elif default_unit.is_file():
            self.userunits = [default_unit]
        else:
            self.userunits = None

    @staticmethod
    def config_menu(screen, title, packages):
        items = []
        for package in packages:
            title = package.name + ' - Configure'
            submenu = ChecklistMenu(screen, title, [
                ('Install', toggle(package, 'install')),
                ('Copy Config', toggle(package, 'install')),
                ('Run Script', toggle(package, 'install')),
                ('Enable Units', toggle(package, 'install'))
            ], True)
            items += [(package.name, toggle(package, 'enabled'), submenu.display)]
        return ChecklistMenu(screen, title, items, True)
                
class Category:
    def __init__(self, name, packages):
        self.name = name
        self.packages = [Package(pkg) for pkg in packages]
        self.enabled = True

    def __repr__(self):
        return self.name + ': ' + str(self.packages)

    @staticmethod
    def config_menu(screen, categories):
        items = []
        for category in categories:
            title = category.name + ' - Configure Packages'
            submenu = Package.config_menu(screen, title, category.packages)
            items += [(category.name, toggle(category, 'enabled'), submenu.display)]
        return ChecklistMenu(screen, 'Configure Categories', items, True)
        
