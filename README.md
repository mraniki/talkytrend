# TalkyTrend 

| <img width="200" alt="Logo" src="https://user-images.githubusercontent.com/8766259/226854338-e900f69e-d884-4a9a-90b1-b3dde7711b31.png"> | A python package to retrieve asset trend and economic data. |
| ------------- | ------------- |
|<br> [![wiki](https://img.shields.io/badge/🪙🗿-wiki-0080ff)](https://talkytrader.gitbook.io/talky/) [![Pypi](https://badgen.net/badge/icon/talkytrend?icon=pypi&label)](https://pypi.org/project/talkytrend/) ![Version](https://img.shields.io/pypi/v/talkytrend)<br>  ![Pypi](https://img.shields.io/pypi/dm/talkytrend)<br> [![Build](https://github.com/mraniki/talkytrend/actions/workflows/%E2%9C%A8Flow.yml/badge.svg)](https://github.com/mraniki/talkytrend/actions/workflows/%E2%9C%A8Flow.yml) [![codecov](https://codecov.io/gh/mraniki/TalkyTrend/branch/main/graph/badge.svg?token=WAHUEMAJN6)](https://codecov.io/gh/mraniki/TalkyTrend) | Find Trend |

Key features:

- trading view connectivity

## Install

`pip install talkytrend`

## How to use it

```
    trend = TalkyTrend()
    result = await trend.fetch_analysis()
    print(result) #BUY
    monitor = await trend.monitor_assets() #monitor change of trend

```

### Example

[example](https://github.com/mraniki/talkytrend/blob/main/examples/example.py)

### Real use case

[TalkyTrader](https://github.com/mraniki/tt)

## Documentation


[![wiki](https://img.shields.io/badge/🪙🗿-wiki-0080ff)](https://talkytrader.gitbook.io/talky/)
