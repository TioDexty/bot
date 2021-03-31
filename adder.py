from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os
import sys
import csv
import traceback
import time
import random

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

print (re+"╔╦╗┌─┐┬  ┌─┐╔═╗  ╔═╗┌┬┐┌┬┐┌─┐┬─┐")
print (gr+" ║ ├┤ │  ├┤ ║ ╦  ╠═╣ ││ ││├┤ ├┬┘")
print (re+" ╩ └─┘┴─┘└─┘╚═╝  ╩ ╩─┴┘─┴┘└─┘┴└─")

print (cy+"version : 1.01")
print (cy+"Certifique-se de ter inscrito @TioDexty no Telegram")
print (cy+"https://t.me/DextyLixo")

print (re+"NOTA :")
print ("1. O Telegram só permite adicionar 200 membros no grupo por um usuário.")
print ("2. Você pode usar várias contas do Telegram para adicionar mais membros.")
print ("3. Adicione apenas 50 membros ao grupo de cada vez, caso contrário, você obterá um erro de inundação. ")
print ("4. Em seguida, aguarde 15-30 mini minutos e adicione membros novamente.")
print ("5. Certifique-se de habilitar Adicionar permissão de usuário em seu grupo")

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] execute python setup.py PRIMEIRO !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Digite o código: '+re))

users = []
with open(r"members.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print(gr+'Escolha um grupo para adicionar membros:'+cy)
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input(gr+"Insira um número: "+re)
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input(gr+"Digite 1 para adicionar por nome de usuário ou 2 para adicionar por ID: "+cy))

n = 0

for user in users:
    n += 1
    if n % 80 == 0:
        sleep(60)
    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Modo inválido selecionado. Por favor, tente novamente.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Esperando por 60-180 segundos...")
        time.sleep(random.randrange(0, 5))
    except PeerFloodError:
        print("Obtendo erro de inundação do telegrama. O script está parando agora. Por favor, tente novamente após algum tempo.")
        print("Esperando {} segundos".format(SLEEP_TIME_2))
        time.sleep(SLEEP_TIME_2)
    except UserPrivacyRestrictedError:
        print("As configurações de privacidade do usuário não permitem que você faça isso. Pulando.")
        print("Esperando por 5 segundos...")
        time.sleep(random.randrange(0, 5))
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue
