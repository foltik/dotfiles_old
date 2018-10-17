#!/usr/bin/python

import parse

categories = parse.parse_package_listing('packages.org')

for category in categories:
    print(category.name)
    for package in category.packages:
        print('- ' + package.name)
