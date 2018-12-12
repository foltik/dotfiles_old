from pathlib import Path
from lib.menu import ChecklistMenu
from lib.path import local_path, deploy_path

def toggle(obj, prop):
    return lambda b: setattr(obj, prop, b)

class Package:
    def __init__(self, obj):
        # Defaults
        self.source = 'core'
        
        # Immutable attributes
        if isinstance(obj, dict):
            self.name, props = next(iter(obj.items()))
            self.alias = self.name
            self.source = 'core'
            for key, value in props.items():
                setattr(self, key, value if value != 'none' else None)
        else:
            self.name = obj
            self.alias = self.name

        # Infer and properly format attributes as paths
        self.check_defaults('config', ['.config/%s'], 'lain/')
        self.check_defaults('script', ['%s.fish'], 'scripts/')
        self.check_defaults('userunit', ['%s.service', '%s@.service'], 'lain/.config/systemd/user/')

        # Install State
        self.enabled = True
        self.install = True
        self.export_config = True
        self.run_script = True
        self.export_units = True
        self.enable_units = True

        
    def __repr__(self):
        return self.name

    def __getitem__(self, key):
        if hasattr(self, key):
            val = getattr(self, key)
            return None if val == 'none' else val
        else:
            return None

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def getattrs(self):
        excepted = [
            'name', 'enabled', 'install',
            'export_config', 'run_script',
            'export_units', 'enable_units'
        ]

        return [(k, v) for k, v in vars(self).items() if v != None and k not in excepted]

    def check_defaults(self, prop, defaults, basepath):
        for default in defaults:
            for name in [self.name, self.alias]: 
                default_path = local_path(basepath, default % name)
                if self[prop]:
                    if isinstance(self[prop], list):
                        self[prop] = list(map(lambda p: local_path(basepath, p), self[prop]))
                    else:
                        self[prop] = [local_path(basepath, self[prop])]
                elif default_path.is_dir() or default_path.is_file():
                    self[prop] = [default_path]
                    
                if self[prop] != None:
                    return

    @staticmethod
    def config_menu(screen, title, packages):
        items = []
        for package in packages:
            title = package.name + ' - Configure'
            submenu = ChecklistMenu(screen, title, [
                ('Install', toggle(package, 'install')),
                ('Export Config', toggle(package, 'export_config')),
                ('Run Script', toggle(package, 'run_script')),
                ('Export Units', toggle(package, 'export_units')),
                ('Enable Units', toggle(package, 'enable_units'))
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
        
