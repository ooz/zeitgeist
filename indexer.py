#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os.path

def as_html(investments):
    return f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zeitgeist</title>
</head>
<body>
<h2>Investments</h2>
<p>Last file update: ~ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
<pre>{investments}</pre>
<p>
<a href="investments.csv">Download csv</a>,
<a href="https://github.com/ooz/zeitgeist">code</a> crafted by <a href="https://ooz.github.io/">ooz</a>,
2019
</p>
</body>
</html>
'''

def readfile(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.read()
    return ''

def main():
    investments_csv = readfile('investments.csv').strip()
    investments_html = as_html(investments_csv)
    with open('index.html', 'w') as f:
        f.write(investments_html)

if __name__ == "__main__":
    main()
