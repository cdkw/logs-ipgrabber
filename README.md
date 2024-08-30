<h1 align="center">Grab player's IPs from a Minecraft log file</h1>

<p align="center">
<a href="#"><img alt="logs-ipgrabber forks" src="https://img.shields.io/github/forks/cdkw/logs-ipgrabber?style=for-the-badge"></a>
<a href="#"><img alt="logs-ipgrabber last commit (main)" src="https://img.shields.io/github/last-commit/cdkw/logs-ipgrabber/main?color=green&style=for-the-badge"></a>
<a href="#"><img alt="logs-ipgrabber Repo stars" src="https://img.shields.io/github/stars/cdkw/logs-ipgrabber?style=for-the-badge&color=yellow"></a>
<a href="#"><img alt="logs-ipgrabber License" src="https://img.shields.io/github/license/cdkw/logs-ipgrabber?color=orange&style=for-the-badge"></a>
<a href="https://github.com/cdkw/logs-ipgrabber/issues"><img alt="logs-ipgrabber issues" src="https://img.shields.io/github/issues/cdkw/logs-ipgrabber?color=purple&style=for-the-badge"></a>

<p align="center">Do not use people's ips for malicious intent without their permission.</p>
<p align="center"><img src="https://i.imgur.com/UXNzI2F.png" alt="Image"></p>


**Requirements**
* Python 3
* A https://ipapi.com api key (free)


**Installing and running**
```shell script
git clone https://github.com/cdkw/logs-ipgrabber.git
cd logs-ipgrabber
pip install -r requirements.txt
python3 fetcher.py -f <file> -v -g
```

Note: Make sure to put your https://ipapi.com key in
```python
# vpn and geolocation
if args.vpn and args.geolocation:
    access_key = 'ACCESS_KEY_HERE!'  ## <-- Put it there!
elif args.vpn...
```



### **☕ Support me!**

If you want to support me, consider joining my discord or donating to my crypto wallets:
* BTC `3QMrNrzGSPunpnYirVFtKp6G4oSnJDk1oT`
* ETH `0xFD03ee7AB099223a4B33327955a9aF3dd3DCDA61`
* SOL `7HDSAnXosAWNiuBwZCv18CdWc9aZCpdNoCBKAf11C7BD`