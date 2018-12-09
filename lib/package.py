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
        self.export_config = True
        self.run_script = True
        self.export_units = True

        
    def __repr__(self):
        return self.name

    def update_from_files(self):
        if self.source == 'none':
            self.source = None
        
        default_config = Path('.config/' + self.name)
        if hasattr(self, 'config'):
            if isinstance(self.config, list):
                self.config = list(map(lambda c: Path(c), self.config))
            elif self.config == 'none':
                self.config = None
            else:
                self.config = Path(self.config)
        elif (Path('lain') / default_config).is_dir():
            self.config = default_config
        else:
            self.config = None
        
        default_script = Path(self.name + '.fish')
        if hasattr(self, 'script'):
            self.script = Path(self.script)
        elif (Path('lain') / default_script).is_file():
            self.script = default_script
        else:
            self.script = None

        default_unit = Path('.config/systemd/user/' + self.name + '.service')
        if hasattr(self, 'userunits'):
            self.userunits = list(map(lambda unit: Path('.config/systemd/user/' + unit), self.userunits))
        elif (Path('lain') / default_unit).is_file():
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
                ('Export Config', toggle(package, 'export_config')),
                ('Run Script', toggle(package, 'run_script')),
                ('Export Units', toggle(package, 'export_units'))
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
        
