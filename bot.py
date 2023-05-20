import telebot
import requests
import os
from bs4 import BeautifulSoup

TOKEN = '6187046471:AAGRy7WmpaaNXk5jkGBMSzIiF69IP0jKMbE'
bot = telebot.TeleBot(TOKEN)

banned_users = set()  # set para guardar usuários banidos
grupo_id = -1001877673753
tmdb_api_key = '50dcb709df1cd8ab0d6399ea2de9c04e'
approved_users = [5479757526, 987654321]

# Mensagem de boas-vindas
WELCOME_MESSAGE = "Olá! Seja bem-vindo(a) ao nosso grupo! Qualquer dúvida, é só perguntar. :)"

# Mensagem de regras
RULES_MESSAGE = "Aqui estão as regras do grupo:\n1. Respeite os outros membros\n2. Não compartilhe conteúdo ofensivo\n3. Não promova atividades ilegais\n4. Seja cordial e evite conflitos\n5. Apenas compartilhe arquivos relacionados aos temas do grupo\nO não cumprimento destas regras pode resultar em banimento do grupo."

# URL da API do TMDb
tmdb_base_url = 'https://api.themoviedb.org/3/'

@bot.message_handler(func=lambda message: message.new_chat_members is not None)
def welcome(message):
    for new_member in message.new_chat_members:
        bot.reply_to(message, WELCOME_MESSAGE.format(new_member.first_name))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá, pessoal! Fico feliz de estar aqui com vocês.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message is not None:
        user_id = message.reply_to_message.from_user.id
        if user_id not in banned_users:
            banned_users.add(user_id)
            bot.reply_to(message, "Usuário {} foi banido!".format(message.reply_to_message.from_user.first_name))
            bot.kick_chat_member(message.chat.id, user_id)
            bot.send_message(message.chat.id, "O usuário {} foi banido do grupo.".format(message.reply_to_message.from_user.first_name))
        else:
            bot.reply_to(message, "Esse usuário já foi banido.")
    else:
        bot.reply_to(message, "Esse comando precisa ser usado em resposta a uma mensagem do usuário a ser banido.")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.reply_to_message is not None:
        user_id = message.reply_to_message.from_user.id
        if user_id in banned_users:
            banned_users.remove(user_id)
            bot.reply_to(message, "Usuário {} foi desbanido!".format(message.reply_to_message.from_user.first_name))
            bot.unban_chat_member(message.chat.id, user_id)
        else:
            bot.reply_to(message, "Esse usuário não está banido.")
    else:
        bot.reply_to(message, "Esse comando precisa ser usado em resposta a uma mensagem do usuário a ser desbanido.")

@bot.message_handler(commands=['rules'])
def rules(message):
    bot.reply_to(message, RULES_MESSAGE)

@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, "Eu sou um bot criado para administrar este grupo! Para saber mais sobre minhas funcionalidades, digite /help.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Aqui estão os comandos disponíveis:\n/start - Inicia o bot\n/ban - Bane um usuário\n/unban - Desbane um usuário\n/rules - Exibe as regras do grupo\n/info - Informações sobre o bot\n/help - Exibe ajuda sobre os comandos\n/id - Exibe o seu ID de usuário")

@bot.message_handler(commands=['id'])
def get_user_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, "Seu ID é: {}".format(user_id))

@bot.message_handler(content_types=['left_chat_member'])
def goodbye(message):
    bot.send_message(message.chat.id, "O usuário {} deixou o grupo.".format(message.left_chat_member.first_name))
    
bot.infinity_polling()