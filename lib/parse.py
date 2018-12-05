import yaml
from pathlib import Path

class Package:
    def __init__(self, obj):
        if isinstance(obj, dict):
            self.name, props = next(iter(obj.items()))
            self.source = 'core'
            for key, value in props.items():
                setattr(self, key, value)
        else:
            self.name = obj
            self.source = 'core'

        self.update_from_files()
        
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
                
class Category:
    def __init__(self, name, packages):
        self.name = name
        self.packages = [Package(pkg) for pkg in packages]
    def __repr__(self):
        return self.name + ': ' + str(self.packages)

def parse(file):
    f = open(file, 'r')
    data = yaml.load(f)
    return [Category(name, packages) for name, packages in data.items()]
