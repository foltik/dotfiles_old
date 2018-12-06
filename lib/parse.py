import yaml
from lib.package import Category, Package

def parse(file):
    f = open(file, 'r')
    data = yaml.load(f)
    return [Category(name, packages) for name, packages in data.items()]
