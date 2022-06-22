from requests import get, post
from sys import argv
from ctypes import windll
import bs4
import base64
from time import sleep
from colorama import init, Fore

init()

sent = 0
total = 0

def Title():
    global sent, total
    windll.kernel32.SetConsoleTitleW(f"[SENT: {sent}/{total}]")

def sender(host: str, token:str, simline: str, msg: str, number: str):
	global sent
	headers = {
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,nl;q=0.6',
	    'Authorization': f'Basic {token}' + "=",
	    'Cache-Control': 'max-age=0',
	    'Connection': 'keep-alive',
	    'Origin': f'http://{host}',
	    'Referer': f'http://{host}/default/en_US/tools.html?type=sms&line=',
	    'Upgrade-Insecure-Requests': '1',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
	}

	params = {
	    'type': 'sms',
	}

	v = get(f"http://{host}/default/en_US/tools.html?type=sms", headers=headers)
	m = bs4.BeautifulSoup(v.text, "html.parser")
	input_tag = m.find_all(attrs={"name" : "smskey"})
	
	if number.startswith("0"):
		number = "+33" + number[1::]

	data = {
	    f'line{simline}': '1',
	    'smskey': input_tag[0]["value"],
	    'action': 'SMS',
	    'telnum': number,
	    'smscontent': msg,
	    'send': 'Send',
	}
	response = post(f'http://{host}/default/en_US/sms_info.html', params=params, headers=headers, data=data, verify=False)
	if "Send successful!" not in response.text:
		print(f"{Fore.YELLOW}Error: {Fore.RED}Not sent")
	else:
		print(f"{Fore.YELLOW}Sent: {Fore.GREEN}" + number)
		sent += 1
		Title()
v = 0
singleornot = int(input("[single:1|numlist:2]> "))

if singleornot == 1:
	msg = input("[msg]> ")
	number = input("[number]>")
	config = open("config.txt", mode="r").read().split("\n")
	for i in config:
		host = i.split("|")[0].split(",")[0]
		token = base64.b64encode(i.split("|")[1].split(",")[0].encode("ascii")).decode("ascii")
		simline = i.split(",")[1]
		sender(host, token, simline, msg, number)
		sleep(0.5)
else:
	msg = input("[msg]> ")
	nl = input("[nl]> ")
	numlist = open(nl, mode="r").read().split("\n")
	config = open("config.txt", mode="r").read().split("\n")
	total = len(numlist)

	for i in range(0, int(len(numlist))):
		v += 1
		host = config[v % len(config)].split("|")[0].split(",")[0]
		token = base64.b64encode(config[v % len(config)].split("|")[1].split(",")[0].encode("ascii")).decode("ascii")
		simline = config[v % len(config)].split(",")[1]
		number = numlist[i]
		sender(host, token, simline, msg, number)
		sleep(0.5)

"""
if __name __ == "__main__":
	msg = "voila" + argv[2]
	inp = input("numlist\n>")
	nl = open(inp, mode="r", encoding="utf-8").read().split("\n")
	sim = open(argv[1], mode="r", encoding="utf-8").read().split("\n")
	m = 0
	for i in nl:
		if i.startswith("0"):
			i = "+33" + i[1::]
		m += 1
		v = get(str(sim[m]).replace(r"{num}", str(i)).replace(r"{msg}", ))
		if "Send SMS to" not in v.text:

			print(f"Sent successfully {i}")
"""
