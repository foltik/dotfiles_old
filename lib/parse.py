import yaml

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
    def __repr__(self):
        return self.name
                
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
