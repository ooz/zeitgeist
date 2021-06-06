#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os.path

# M1 Chart: https://levels.io/m1-chart/
def as_markdown(investments, news):
    return f'''---
title: Zeitgeist
tags: __no_header__, __no_footer__
---

# [Zeitgeist](https://oliz.io/zeitgeist/) [![Zeitgeist CircleCI build indicator](https://circleci.com/gh/ooz/zeitgeist.svg?style=shield)](https://circleci.com/gh/ooz/zeitgeist)

## Language

{news}

## Investments[.csv](investments.csv)

[Inflation Chart](https://inflationchart.com),
[Stocks in BTC](https://stonksinbtc.xyz/)

```
{investments}
```

<footer>
<a href="javascript:toggleTheme()" class="nav">🌓</a>
- <a href="https://github.com/ooz/zeitgeist">code</a> measuring the Zeitgeist since 2019, by <a href="https://oliz.io">oz</a>
</footer>
'''

def readfile(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.read()
    return ''

def main():
    investments_csv = readfile('investments.csv').strip()
    news = readfile('news.html').strip()
    index_md = as_markdown(investments_csv, news)

    with open('README.md', 'w') as f:
        f.write(index_md)

if __name__ == "__main__":
    main()
