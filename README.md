# TalkyTrend 

| <img width="200" alt="Logo" src="https://user-images.githubusercontent.com/8766259/226854338-e900f69e-d884-4a9a-90b1-b3dde7711b31.png"> | A python package to retrieve asset trend and economic data. |
| ------------- | ------------- |
|<br> 
[![wiki](https://img.shields.io/badge/🪙🗿-wiki-0080ff)](https://talkytrader.gitbook.io/talky/) [![Pypi](https://badgen.net/badge/icon/talkytrend?icon=pypi&label)](https://pypi.org/project/talkytrend/) [![Version](https://img.shields.io/pypi/v/talkytrend)]()<br> [![Pypi](https://img.shields.io/pypi/dm/talkytrend)]()<br> [![👷‍♂️Build](https://github.com/mraniki/talkytrend/actions/workflows/%F0%9F%91%B7%E2%80%8D%E2%99%82%EF%B8%8FFlow.yml/badge.svg)]() <br>[![codecov](https://codecov.io/gh/mraniki/TalkyTrend/branch/main/graph/badge.svg?token=WAHUEMAJN6)](https://codecov.io/gh/mraniki/TalkyTrend) [![codebeat badge](https://codebeat.co/badges/24c90aab-02d7-4cd1-9ad8-5907e180c9e6)](https://codebeat.co/projects/github-com-mraniki-talkytrend-main) | Find Asset Trend |

Key features:

- trading view connectivity

## Install

`pip install talkytrend`

## How to use it

```
    talky = TalkyTrend()
    result = await talky.check_signal()
    <!-- BUY -->

    result = await talky.fetch_key_events()
    print(result)
    <!-- Title:  FDA advisers say new Alzheimer’s drug lecanemab slows cognitive decline -->
    <!-- Description:  Panel’s opinion could pave way for full regulatory approval next month for treatment of disease that affects 6.5m Americans -->

    monitor = await talky.scanner() #ongoing monitoring
    <!-- New signal for BTCUSD (4h): STRONG_SELL -->
    <!-- Key event: {'title': 'OPEC-JMMC Meetings', 'country': 'ALL', 'date': '2023-06-04T06:15:00-04:00', 'impact': 'High', 'forecast': '', 'previous': ''} -->
    <!-- Key news: FDA advisers say new Alzheimer’s drug lecanemab slows cognitive decline -->
```

### Example

[example](https://github.com/mraniki/talkytrend/blob/main/examples/example.py)

### Real use case

[TalkyTrader](https://github.com/mraniki/tt)

## Documentation


[![wiki](https://img.shields.io/badge/🪙🗿-wiki-0080ff)](https://talkytrader.gitbook.io/talky/)
