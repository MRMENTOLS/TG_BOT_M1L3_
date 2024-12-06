import config
import telebot
import random
import requests

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['fact'])
def send_fact(message):
  try:
    response = requests.get("http://official-joke-api.appspot.com/random_joke")
    response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json()
    # This API returns a joke, not a fact, but we'll use the setup as a fact-like statement
    fact = data['setup'] #Using setup as a 'fact' for simplicity
    bot.reply_to(message, fact)
  except requests.exceptions.RequestException as e:
    bot.reply_to(message, f"Error fetching fact: {e}")
  except (KeyError, IndexError) as e: # Handle potential missing keys in JSON response.
    bot.reply_to(message, f"Error parsing fact data: {e}")


bot.infinity_polling()