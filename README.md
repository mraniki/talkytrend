
<br>
<table style="border: 1px solid transparent">
  
  <tr>
    <td>
<a href="http://talky.readthedocs.io"><img src="https://img.shields.io/badge/Wiki-%23000000.svg?style=for-the-badge&logo=wikipedia&logoColor=white"></a>
<a href="https://github.com/mraniki/tt/"><img src="https://img.shields.io/badge/github-%23000000.svg?style=for-the-badge&logo=github&logoColor=white"></a><br>
<a href="https://hub.docker.com/r/mraniki/tt"><img src="https://img.shields.io/docker/pulls/mraniki/tt?style=for-the-badge"></a><br>
       </td>
    <td align="center"><img width="200" alt="Logo" src="https://user-images.githubusercontent.com/8766259/226854338-e900f69e-d884-4a9a-90b1-b3dde7711b31.png"></td>
  </tr>
  <tr>
    <td>
      <a href="https://pypi.org/project/talkytrend/"><img src="https://img.shields.io/pypi/v/talkytrend?style=for-the-badge&logo=PyPI&logoColor=white"></a><br>
      <a href="https://pypi.org/project/talkytrend/"><img src="https://img.shields.io/pypi/dm/talkytrend?style=for-the-badge&logo=PyPI&logoColor=white"></a><br>
      <a href="https://github.com/mraniki/talkytrend/"><img src="https://img.shields.io/github/actions/workflow/status/mraniki/talkytrend/%F0%9F%91%B7Flow.yml?style=for-the-badge&logo=GitHub&logoColor=white"></a><br>
      <a href="https://talky.readthedocs.io/projects/talkytrend/"><img src="https://readthedocs.org/projects/talkytrend/badge/?version=latest&style=for-the-badge"></a><br>
      <a href="https://codebeat.co/projects/github-com-mraniki-talkytrend-main"><img src="https://codebeat.co/badges/24c90aab-02d7-4cd1-9ad8-5907e180c9e6"/></a> <br>
      <a href="https://codecov.io/gh/mraniki/talkytrend"><img src="https://codecov.io/gh/mraniki/talkytrend/branch/main/graph/badge.svg?token=WAHUEMAJN6"/></a><br>
    </td>
    <td align="left"> 
Retrieve asset trend and economic data.<br>
Trading view connectivity<br>
News connectivity<br>
       FOMC reminder<br>
    </td>
     
  </tr>
</table>


<h5>How to use it</h5>
<pre>
<code>
    talky = TalkyTrend()
    result = await talky.fetch_signal()
    #  BUY
    result = await talky.fetch_event()
    print(result)
    #  Title:  FDA advisers say new Alzheimer’s drug lecanemab slows cognitive decline
    # Description:  Panel’s opinion could pave way for full regulatory approval next month for treatment of disease that affects 6.5m Americans
    monitor = await talky.monitor() #ongoing monitoring
    # New signal for BTCUSD (4h): STRONG_SELL
    # Key event: {'title': 'OPEC-JMMC Meetings', 'country': 'ALL', 'date': '2023-06-04T06:15:00-04:00', 'impact': 'High', 'forecast': '', 'previous': ''}\
    # Key news: FDA advisers say new Alzheimer’s drug lecanemab slows cognitive decline
</code>
</pre>
</details>

<h5>Documentation</h5>
<a href="https://talky.readthedocs.io/projects/talkytrend/en/latest/"><img src="https://img.shields.io/badge/Documentation-000000?style=for-the-badge&logo=readthedocs&logoColor=white"></a><br>

