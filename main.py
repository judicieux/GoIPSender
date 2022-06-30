from requests import get, post
from sys import argv
import ctypes
import bs4
import base64
from time import sleep
from colorama import init, Fore
from os import system, name
import pymysql


init()
sent = 0
total = 0

def clear():
	system("cls" if name == "nt" else "clear")

def Title():
	global sent, total
	ctypes.windll.kernel32.SetConsoleTitleW(f"[SENT: {sent}/{total}]")

def clearInbox(host: str, token:str):
	headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,nl;q=0.6',
    'Authorization': f'Basic {token}' + '=',
    'Connection': 'keep-alive',
    'Referer': f'http://{host}/default/en_US/tools.html?action=del&type=sms_inbox&line=-1&pos=-1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
	}

	params = {
	    'type': 'sms_inbox',
	    'code': 'utf8',
	    'line': '-1',
	}

	response = get(f'http://{host}/default/en_US/tools.html', params=params, headers=headers, verify=False)

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
		print(f"{Fore.YELLOW}Sent: {Fore.GREEN}" + number + f"{Fore.RESET}")
		sent += 1
		Title()

ctypes.windll.kernel32.SetConsoleTitleW(f"eSIMGate SENDER - BY @siliconesolidity")
key = input("[Access_Key]: ")
connection = pymysql.connect(
	user='toronto', 
	passwd='Kaka123.', 
	host='mysql-toronto.alwaysdata.net', 
	database='toronto_apache'
)

cursor = connection.cursor()
query = (f"SELECT * FROM sender_access_keys WHERE access_key = '{key}'")
cursor.execute(query)
connect = [str(i) for i in cursor]

if connect:
	v = 0
	while True:
		ctypes.windll.kernel32.SetConsoleTitleW(f"eSIMGate SENDER - BY @siliconesolidity")
		clear()
		
		print(r"""

	 _______      _______ _________ _______  _______  _______ _________ _______ 
	(  ____ \    (  ____ \\__   __/(       )(  ____ \(  ___  )\__   __/(  ____ \
	| (    \/    | (    \/   ) (   | () () || (    \/| (   ) |   ) (   | (    \/
	| (__  _____ | (_____    | |   | || || || |      | (___) |   | |   | (__    
	|  __)(_____)(_____  )   | |   | |(_)| || | ____ |  ___  |   | |   |  __)   
	| (                ) |   | |   | |   | || | \_  )| (   ) |   | |   | (      
	| (____/\    /\____) |___) (___| )   ( || (___) || )   ( |   | |   | (____/\
	(_______/    \_______)\_______/|/     \|(_______)|/     \|   )_(   (_______/
	                                                                            
				t.me/eSIMGate | @siliconesolidity
		""")
		
		singleornot = int(input("[single]: 1 | [numlist]: 2\n> "))

		if singleornot == 1:
			number = input("[Number]> ")
			msg = input("[Message]> ")
			config = open("config.txt", mode="r").read().split("\n")
			config[0] = base64.b64decode(config[0]).decode()
			total = 1

			for i in config:
				host = i.split("|")[0].split(",")[0]
				token = base64.b64encode(i.split("|")[1].split(",")[0].encode("ascii")).decode("ascii")
				simline = i.split(",")[1]
				sender(host, token, simline, msg, number)
				sleep(2)
				clearInbox(host, token)
		else:
			nl = input("[Numlist]> ")
			msg = input("[Message]> ")
			numlist = open(nl, mode="r").read().split("\n")
			config = open("config.txt", mode="r").read().split("\n")
			config[0] = base64.b64decode(config[0]).decode()
			total = len(numlist)

			for i in range(0, int(len(numlist))):
				v += 1
				host = config[v % len(config)].split("|")[0].split(",")[0]
				token = base64.b64encode(config[v % len(config)].split("|")[1].split(",")[0].encode("ascii")).decode("ascii")
				simline = config[v % len(config)].split(",")[1]
				number = numlist[i]
				sender(host, token, simline, msg, number)
				sleep(2)
				clearInbox(host, token)

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
