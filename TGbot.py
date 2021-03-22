import time
import random
import telebot
import requests
import bs4
import re

TOKEN = "own_token_here"
bot = telebot.TeleBot(TOKEN)

def extract_arg(arg):
    return arg.split()[1:]

def get_food_items(foodItems):

    temp = " "
    temp = temp.join(foodItems)

    foodList = temp.split(",")

    print(foodList)

    foodDictionary = {}
    for item in foodList:
        kcal = get_food_nutrition(item)

        if kcal == 0:
            foodDictionary[item] = "Ei hakutuloksia"
        else:
            foodDictionary[item] = kcal

    return foodDictionary


def get_food_nutrition(hakusana):

    hakusana = re.sub(r"[^\w\s]", '', hakusana)
    hakusana = re.sub(r"\s+", '+', hakusana)

    url = "https://www.kilokalori.net/ravinto/kaloritaulukko?q="
    url2 = "&sortBy=totalCount&sortOrder=desc&page=1"
    response = requests.get(url + hakusana + url2)

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    content = soup.findAll("div", {"class": "nutrition-col"})

    try:
        first = str(content[0]).strip('</div>')
        kcal = first.split("/> ")
        lukema = kcal[1]

        return lukema
    except:
        return 0

def calculate_total_cals(foodDictionary):

    total_cals = 0

    for key in foodDictionary:

        kcal = ''.join(filter(str.isdigit, foodDictionary[key]))

        print("Kalorit: "+ kcal)

        if kcal.isdigit():
            total_cals += int(kcal)

    if int(total_cals) > 1000:
        message_text = "Yhteensä: " + str(total_cals) + "kcal. Yli tuhat kcal!" + "\n"
        return message_text
    elif int(total_cals) > 800:
        message_text = "Yhteensä: " + str(total_cals) + "kcal. Yli 800 kcal." + "\n"
        return message_text
    elif int(total_cals) > 600:
        message_text = "Yhteensä: " + str(total_cals) + "kcal. Yli 600 kcal." + "\n"
        return message_text
    elif int(total_cals) > 400:
        message_text = "Yhteensä: " + str(total_cals) + "kcal. Yli 400 kcal." + "\n"
        return message_text
    else:
        message_text = "Yhteensä: " + str(total_cals) + "kcal. Alle 400 kcal." + "\n"
        return message_text



@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, '"Kirjoita /arvostele ja arvosteltavat ruoka-aineet komennon perään pilkulla eroteltuna \n Esim: /arvostele sukaakeksi, irtokarkki"')

@bot.message_handler(commands=['arvostele']) # welcome message handler
def arvostele(message):
    foodItems = extract_arg(message.text)
    print(foodItems)

    if len(foodItems) == 0:
        bot.reply_to(message, "Kirjoita /arvostele ja arvosteltavat ruoat komennon perään pilkulla eroteltuna \nEsim: /arvostele Suklaa")
    else:

        foodDictionary = get_food_items(foodItems)

        total_cals = calculate_total_cals(foodDictionary)

        message_text = "Annettujen ruokien löydetty kalorimäärä:\n"
        for key in foodDictionary:
            message_text += "Annettu ruoka: "+key+", Kcal: "+ foodDictionary[key]+"\n"

        message_text += total_cals

        print(message.chat.first_name + " "+message.chat.last_name+ " viesti: "+ message_text)
        print(message)

        bot.reply_to(message, message_text)


@bot.message_handler(commands=['help'])
def send_welcome_message(message):
    bot.reply_to(message, 'Kirjoita /arvostele ja arvosteltavat ruoat komennon perään pilkulla eroteltuna \nEsim: /arvostele Suklaa')


while True:
    try:
        bot.polling(none_stop=True)

    except Exception:
        time.sleep(15)