#!/usr/bin/python

class Package:
    def __init__(self, line):
        self.type = line[0]
        self.name = line[1]
        self.script = line[2] if len(line) == 3 else None
    type = None
    name = None
    script = None

class Category:
    def __init__(self, line):
        self.name = ' '.join(line[1:])
        self.packages = []
    name = ''
    packages = []

def parse_package_listing(file):
    f = open(file, 'r')
    lines = list(map(lambda l: l.rstrip().split(' '), f.readlines()))
    categories = []
    category = None
    for line in lines:
        if line[0].startswith('*'):
            category = Category(line)
            categories.append(category)
        elif len(line[0]) != 0:
            category.packages.append(Package(line))
    return categories
