#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os.path

def as_html(investments, weather):
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
<pre>{investments}</pre>
<p><a href="investments.csv">Download csv</a></p>

<h2>Weather</h2>
<p><a href="https://de.wttr.in/Leipzig?3mFq" target="_blank">Leipzig</a>,
<a href="https://de.wttr.in/Hamburg?3mFq" target="_blank">Hamburg</a>,
<a href="https://de.wttr.in/Jena?3mFq" target="_blank">Jena</a></p>
<pre>{weather}</pre>

<p>
Last update: ~ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC,
<a href="https://github.com/ooz/zeitgeist">code</a> crafted by <a href="https://ooz.github.io/">ooz</a>, 2019</p>
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
    weather = readfile('weather.txt').strip()
    investments_html = as_html(investments_csv, weather)
    with open('index.html', 'w') as f:
        f.write(investments_html)

if __name__ == "__main__":
    main()
