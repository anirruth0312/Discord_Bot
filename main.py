from http import client
from dotenv import load_dotenv
from multiprocessing.connection import Client
import os
import discord
import requests
import json
import random
from googlesearch import search

load_dotenv()

client = discord.Client()

bad_words = ["fuck", "moron", "jerk", "idiot"]

# lists of roasts
roast = ["YOU'RE SO UGLY HELLO KITTY SAID GOODBYE TO YOU", "YOUR FAMILY TREE IS A CACTUS, BECAUSE EVERYBODY ON IT IS A PRICK",
         "Oops, my bad. I could’ve sworn I was dealing with an adult.", "You’re the reason God created the middle finger",
         "Your face makes onions cry.", "Light travels faster than sound which is why you seemed bright until you spoke",
         "There is someone out there for everyone. For you, it’s a therapist.", "All mistakes are fixable, yet you aren’t.",
         "Whoever told you to be yourself, gave you a bad advice.", "Honey, only thing bothering me is placed between your ears.", "Earth is full. Go home",
         "It is better to shut your mouth and make people think you are stupid than open it and remove all doubt",
         "A glowstick has a brighter future than you. Lasts longer in bed, too"]

help_message = '''```Use "$"followed by any command.\n\n1.help : List of all commands the bot responds to. 
2.inspire : Use this command to generate an inspirational quote. 
3.roast : Use this command to generate an insult
4.bmi : Use this command to find out bmi.
Syntax is : $bmi "height" "weight" "inch/cm"  unit is either in cm/kgs or inches/pounds.
5.search :use this command followed by a word or phrase you want to google```'''


def quote():
    response = requests.get("https://zenquotes.io/api/random")
    # loading the response into json_data
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return quote


def bmi(h, w, unit):
    bmi = 0
    w = int(w)
    h = int(h)
    if (unit == "inch"):
        bmi = ((w / (h * h)) * 703 * 1000)
        bmi = bmi / 1000
    elif (unit == "cm"):
        bmi = (w / (h * h)) * 10000
    bmi = round(bmi, 2)
    bmi_status = ""
    if (bmi >= 30):
        bmi_status = "Obese"
    elif (bmi >= 25):
        bmi_status = "OverWeight"
    elif (bmi >= 18.5):
        bmi_status = "Normal Weight"
    else:
        bmi_status = "UnderWeight"
    bmiarray = []
    bmiarray.append(bmi)
    bmiarray.append(bmi_status)
    return bmiarray


def google_search(query):
    ans = search(query, lang='en',num_results=5)
    return ans


@client.event
async def on_ready():
    print("Logged in as {0.user}!!".format(client))
# welcoming a member


@client.event
async def on_member_join(member):
    await member.send("Hi {member.name} welcome to the server")

# message events


@client.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user:  # when the message is sent by the bot itself
        return
    elif msg.startswith("help"):
        await message.channel.send(help_message)
    elif msg.startswith('hello') or msg.startswith('hi'):
        await message.channel.send('Hello ' + message.author.name)
        # send the message to the particular channel
    elif msg.startswith('bye'):
        await message.channel.send('Goodbye ' + message.author.name)
    elif msg.startswith('$inspire'):
        inspire_quote = quote()
        await message.channel.send(inspire_quote)
    elif any(word in msg.lower() for word in bad_words):
        await message.channel.send(message.author.name + " please dont use abusive language.")
    elif msg.startswith('$roast'):
        await message.channel.send(random.choice(roast))
    elif msg.startswith("$bmi"):
        arr = msg.split()
        height = arr[1]
        weight = arr[2]
        unit = arr[3]
        result = bmi(height, weight, unit)
        await message.channel.send("Your bmi is {} and your weight status is {}".format(result[0], result[1]))
    elif msg.startswith('$search'):
        answer = message.content
        answer.replace('$search', '')
        result = google_search(answer)
        for i in result:
            print(i)
            await message.channel.send(i)
client.run(os.getenv("TOKEN"))
