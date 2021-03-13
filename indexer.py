#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os.path

def as_html(investments, news):
    return f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zeitgeist</title>
<link rel="stylesheet" href="static/oz.css">
</head>
<body>

<h2>Language</h2>
{news}

<details>
<summary><h2>Investments<a href="investments.csv">.csv</a></h2></summary>
<p><a href="https://m1chart.com" target="_blank">M1 Chart</a>, <a href="https://stonksinbtc.xyz/" target="_blank">Stocks in BTC</a></p>
<pre><code>{investments}
</code></pre>
</details>

<p>
- measuring the
<a href="https://github.com/ooz/zeitgeist">Zeitgeist</a>
<a href="https://circleci.com/gh/ooz/zeitgeist" target="_blank"><img src="https://circleci.com/gh/ooz/zeitgeist.svg?style=shield" alt="Zeitgeist CircleCI build indicator" /></a>
since 2019, by <a href="https://oliz.io">oz</a></p>
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
    news = readfile('news.html').strip()
    investments_html = as_html(investments_csv, news)
    with open('index.html', 'w') as f:
        f.write(investments_html)

if __name__ == "__main__":
    main()
