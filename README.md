# TalkyTrend 
![Trend](https://user-images.githubusercontent.com/8766259/226854338-e900f69e-d884-4a9a-90b1-b3dde7711b31.png)


Retrieve key economic data such as Trend, Key economic data for any financial symbol thru messaging platform.

## Build status
[![Docker](https://github.com/mraniki/tt/actions/workflows/DockerHub.yml/badge.svg)](https://github.com/mraniki/tt/actions/workflows/DockerHub.yml) 

## Install

### Docker
	docker push mraniki/talkytrend:latest

or 
	
	docker pull ghcr.io/mraniki/talkytrend:latest

### Local
	git clone https://github.com/mraniki/talkytrend:main && pip install -r requirements.txt



	python3 bot.py

### Environment .env

	#LOG LEVEL
	LOGLEVEL=DEBUG
	
	#TWELVE DATA API
	TDAPI=123
	
	#FINNHUB API
	FNAPI=123
	
	#FREDAPI
	FRAPI=123

	#FASTAPI WEBSERVER PORT & IP
	PORT=
	HOST=

## Features
🚧 WiP

## Questions? Want to help? 

[![discord](https://badgen.net/badge/icon/discord/purple?icon=discord&label)](https://discord.gg/vegJQGrRRa)
[![telegram](https://badgen.net/badge/icon/telegram?icon=telegram&label)](https://t.me/TTTalkyTraderChat/1)
