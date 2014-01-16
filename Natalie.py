import praw
import pywapi
import re
import urllib2
import shutil
import mp3play
import os
from time import sleep
from time import strftime

weatherresult = []
wnews = []
news = []
weathervoice = []
voiceout = []
i = 0
newline = []
directory = r'C:\Users\me\PycharmProjects\NatalieDAA'


def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)


def cleanin(title):
    title = removeNonAscii(title)
    clean = re.sub('[\)\:\\\'\.\\"\(\-\_\+\=\!\@\$\%\^\&\*\|\[\]\{\}\;\<\>\,\/\~\`]', '', title)
    return str(clean)


def getweather():
    print 'Pulling weather data from NOAA'
    noaa = pywapi.get_weather_from_noaa('KRFD')
    weatherresult.append(noaa['weather'].lower())
    weatherresult.append(noaa['temp_f'])
    weatherresult.append(noaa['wind_mph'])

def getreddits():
    print 'Getting hot topics on Reddit'
    reddit = praw.Reddit(user_agent='Data Aggregation Bot')
    for submission in reddit.get_subreddit('technology').get_hot(limit=3):
        each = cleanin(submission.title)
        news.append(each)
    for submission in reddit.get_subreddit('worldnews').get_hot(limit=4):
        each = cleanin(submission.title)
        news.append(each)
    for submission in reddit.get_subreddit('news').get_hot(limit=3):
        each = cleanin(submission.title)
        news.append(each)
    news.remove(news[3])
    news.append("That's all the news for right now")
    news.append("Have a nice day")


def printout():
    weathervoice.append("Good Morning Jeff")
    weathervoice.append("Today's date is " + strftime("%A %B %d"))
    weathervoice.append("The time is " + strftime("%I") + " oclock and " + strftime("%M") + " minutes")
    weathervoice.append("Today's weather from the National Oceanic and Atmospheric Administration is " + weatherresult[0])
    weathervoice.append("It is " + weatherresult[1] + " degrees Fahrenheit")
    weathervoice.append("Wind speed is " + weatherresult[2] + " Miles Per Hour")
    weathervoice.append("Top news from Reddit right now is")


def tts():
    i = 0
    print "Getting TTS data"
    for each in voiceout:
        url = "http://translate.google.co.uk/translate_tts?tl=en&q=" + each
        request = urllib2.Request(url)
        request.add_header('User-agent', 'Mozilla/5.0')
        opener = urllib2.build_opener()
        f = open("data" + str(i) + ".mp3", "wb")
        f.write(opener.open(request).read())
        f.close()
        i = i + 1

def transprep(input):
    i = 0
    newline = []
    for each in input:
        word = each.split()
        for each in word:
            i = i + (len(each) + 1)
            if i < 100:
                newline.append(each)
            else:
                voiceout.append("+".join(newline))
                del newline[:]
                newline.append(each)
                i = len(each) + 1
        voiceout.append("+".join(newline))
        i = 0
        del newline[:]


def cat():
    i = len(voiceout)
    n = 0
    print "Concatinating mp3 files"
    destination = open('morning.mp3', 'wb')
    while i > 0:
        shutil.copyfileobj(open("data" + str(n) + ".mp3",'rb'), destination)
        os.remove('data' + str(n) +".mp3")
        n = n + 1
        i = i - 1
    destination.close()

def speak():
    print "Speaking at you..."
    mp3 = mp3play.load('morning.mp3')
    mp3.play()
    while mp3.isplaying():
        sleep(1)
    os.remove('morning.mp3')



getreddits()
getweather()
printout()
transprep(weathervoice)
transprep(news)
tts()
cat()
speak()