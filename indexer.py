#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os.path

# M1 Chart: https://levels.io/m1-chart/
def as_html(investments, news):
    return f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="script-src 'unsafe-inline'">
<meta name="referrer" content="no-referrer">
<title>Zeitgeist</title>
<link rel="stylesheet" type="text/css" href="https://raw.githubusercontent.com/ooz/templates/master/css/oz.css">
{darkmode_script_from_ggpy()}
</head>
<body onload="initTheme()">

<h2>Language</h2>
{news}

<h2>Investments<a href="investments.csv">.csv</a></h2>
<p><a href="https://inflationchart.com" target="_blank">Inflation Chart</a>, <a href="https://stonksinbtc.xyz/" target="_blank">Stocks in BTC</a></p>
<pre><code>{investments}
</code></pre>

<p>- measuring the
<a href="https://github.com/ooz/zeitgeist">Zeitgeist</a>
<a href="https://circleci.com/gh/ooz/zeitgeist" target="_blank"><img src="https://circleci.com/gh/ooz/zeitgeist.svg?style=shield" alt="Zeitgeist CircleCI build indicator" /></a>
since 2019, by <a href="https://oliz.io">oz</a>, <a href="javascript:toggleTheme()" class="nav">🌓</a>
</p>
</body>
</html>
'''

def darkmode_script_from_ggpy():
    '''See https://oliz.io/ggpy/
    '''
    return '''<script>
function toggleTheme() { document.body.classList.toggle("dark-mode") }
function initTheme() { let h=new Date().getHours(); if (h <= 8 || h >= 20) { toggleTheme() } }
</script>'''

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
