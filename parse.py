#!/usr/bin/python
import re

class Package:
    def __init__(self, line):
        self.type = line[0]
        self.name = line[1]
        self.script = line[2] if len(line) == 3 else None
    @staticmethod
    def is_package_line(line):
        return re.match(r"^[^*]+", line[0])

class Category:
    def __init__(self, line):
        self.name = ' '.join(line[1:])
        self.packages = []
    @staticmethod
    def is_category_line(line):
        return re.match(r"^\*+", line[0])

def split(lines):
    return list(map(lambda line: line.rstrip().split(' '), lines))

def parse_package_listing(file):
    f = open(file, 'r')
    categories = []
    category = None
    for line in split(f.readlines()):
        if Category.is_category_line(line):
            category = Category(line)
            categories.append(category)
        elif Package.is_package_line(line):
            category.packages.append(Package(line))
    return categories
