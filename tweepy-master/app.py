# -*- coding: utf-8 -*-
"""
Spyder Editor

SMT-Ass2: Differences in nutrition habits among the US
@author: Markus
"""

from tweepy import Stream
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import TweepError

import time
from datetime import datetime, timedelta
#import jsonpickle
import json

ckey = '6IdDhRCLKr9gUBQ50NHVciiHw'
csecret = 'n4mGBOE67xojpGFldtzkQWHN6Udkc6bpTY0rVGgvNoYAEBJaZg'
atoken = '3865326437-emzK4kEVZXixi95VrxuAiCLXFICKzziSR59ORxp'
asecret = 'vJUWdWjPJpz5uX1aL2wynnbbD2er3lrKc0iDnpJEBAmPn'

searchQueries = []
searchQueries.append('place:96683cc9126741d1 #dinner OR #breakfast OR #lunch OR #brunch OR #snack OR #meal OR #supper OR #drinks OR #rvadine OR #pizza OR #food OR #bento OR #beer OR #fresh OR #cooking OR #dessert OR #foodporn OR #paleo OR #restaurant OR #tapas OR #vegan OR #yum OR #yummy')
searchQueries.append('place:96683cc9126741d1 #bacon OR #healthy OR #delicious OR #bbq OR #foodie OR #vegetarian OR #goodeats OR #cltfood OR #kosher OR #streetfood OR #foodgasm OR #chefmode OR #hungry OR #cleaneating OR #EEEEEATS OR #truecooks OR #yougottaeatthis OR #eatfamous OR #foodstagram')
searchQueries.append('place:96683cc9126741d1 #eats OR #igfood OR #foodphotography OR #buzzfeedfood OR #feedfeed OR #huffposttaste OR #foodbloggers OR #yummie OR #tastespotting OR #foodgawker OR #instayum OR #instafood OR #foodlove OR #foodies OR #homecooking OR #cleandiet OR #foodblog')
searchQueries.append('place:96683cc9126741d1 #foodblogger OR #truecooks OR #instaphoto OR #foodvsco OR #foodpics OR #foodlover OR #foodforthought OR #foodisfuel OR #foodcoma OR #fooddiary OR #foodgram OR #foodspotting OR #foodshare OR #foodart OR #foodforfoodies OR #foodoftheday OR #foodstyling')
searchQueries.append('place:96683cc9126741d1 #foodism OR #foodaddict OR #foodography OR #foodtime OR #eatclean OR #eating OR #eathealthy OR #eatwell OR #eatright OR #eatingclean OR #eatinghealthy OR #eatgood OR #eattherainbow OR #eatrealfood OR #eatstagram OR #yummie OR #yumm OR #yumyum')
searchQueries.append('place:96683cc9126741d1 #yummi OR #yummm OR #yummyinmytummy OR #yummmm OR #yummyfood OR #yumyumyum OR #yums OR #desserts OR #dinnertime OR #dinnerisserved OR #bread OR #lunchtime OR #lunchbreak')
maxTweets = 1000000
tweetsPerQuery = 2500
# max 100 tweets per query - 450 queries every 15 minutes -> 45,000 tweets every 15 minutes
fileName = 'TwitterData.json'
now = datetime.now()

do_stream = True

class listener(StreamListener):
    def on_data(self, data):
        try:
            #print (data)
            
            tweet = data.split(',"text":"')[1].split('"source')[0]
            #print (tweet)
            
            d = json.loads(data)
            if ((d['place'] is not None) or (d['user']['time_zone'] is not None) or (d['user']['location'] is not None)):
                printDataToFile(data)
                print(d['text'])
                #print(d['place'])
                #print(d['user']['time_zone'])
                #print(d['user']['location'])
            #saveThis = str(time.time())+'::'+tweet
            #print (saveThis)
            
            return True
        except BaseException as e:
            print ('failed ondata', str(e))
            time.sleep(5)
    
    def on_error(self, status):
        print (status)
        
def printDataToFile(data):
    saveFile = open('TwitterData_stream.json', 'a')
    saveFile.write(data)
    saveFile.close()
    
def limitHandled(cursor):
    while True:
        try:
            yield cursor.next()
        except TweepError as e:
            print ('sleeping for 15 minutes. ', str(e))
            time.sleep(15 * 60)
        
def stream(N):
    d_since = datetime.now() - timedelta(days=N)
    d_until = datetime.now() - timedelta(days=N-1)
    try:
        if do_stream: #Streaming API
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=['#dinner', '#breakfast', '#lunch', '#brunch', '#snack', '#meal', '#supper', '#drinks', '#rvadine', '#pizza', '#food', '#bento', '#beer', '#fresh', '#cooking', '#dessert', '#foodporn', '#paleo', '#restaurant', '#tapas', '#vegan', '#yum', '#yummy', '#bacon', '#healthy', '#delicious', '#bbq', '#foodie', '#vegetarian', '#goodeats', '#cltfood', '#kosher', '#streetfood', '#foodgasm', '#chefmode', '#hungry', '#cleaneating', '#EEEEEATS', '#truecooks', '#yougottaeatthis', '#eatfamous', '#foodstagram', '#eats', '#igfood', '#foodphotography', '#buzzfeedfood', '#feedfeed', '#huffposttaste', '#foodbloggers', '#yummie', '#tastespotting', '#foodgawker', '#instayum', '#instafood', '#foodlove', '#foodies', '#homecooking', '#cleandiet', '#foodblog', '#foodblogger', '#truecooks', '#instaphoto', '#foodvsco', '#foodpics', '#foodlover', '#foodforthought', '#foodisfuel', '#foodcoma', '#fooddiary', '#foodgram', '#foodspotting', '#foodshare', '#foodart', '#foodforfoodies', '#foodoftheday', '#foodstyling', '#foodism', '#foodaddict', '#foodography', '#foodtime', '#eatclean', '#eating', '#eathealthy', '#eatwell', '#eatright', '#eatingclean', '#eatinghealthy', '#eatgood', '#eattherainbow', '#eatrealfood', '#eatstagram', '#yummie', '#yumm', '#yumyum', '#yummi', '#yummm', '#yummyinmytummy', '#yummmm', '#yummyfood', '#yumyumyum', '#yums', '#desserts', '#dinnertime', '#dinnerisserved', '#bread', '#lunchtime', '#lunchbreak'])
            #twitterStream.filter(locations=[-125,25,-65,48], async=False)
        else: #REST API
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            api = API(auth)
            saveFile = open(fileName, 'a')
            maxTweetCount = 0
            for idx, query in enumerate(searchQueries):
                tweetCount = 0
                for tweet in limitHandled(Cursor(api.search, q=query, since=d_since.strftime("%Y-%m-%d"), until=d_until.strftime("%Y-%m-%d"), lang='en').items()):
                    if tweet.place is not None:
                        #saveFile.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
                        tweetCount += 1
                        maxTweetCount += 1
                print("Downloaded {0} tweets for Q{1}. since {2} until {3}".format(tweetCount, idx, d_since.strftime("%Y-%m-%d"), d_until.strftime("%Y-%m-%d")))
                    
            saveFile.close()
            
            #print(jsonpickle.encode(tweet._json, unpicklable=False), '\n')
            print("Downloaded {0} tweets for {1} queries in total".format(maxTweetCount, len(searchQueries)))
            #results = api.search(q=searchQuery1, count=1, lang='en', result_type='recent')
            #print ('results: ', results)
            
    except TweepError as e:
        print('tweep error: ', str(e))
        time.sleep(100)
        
max_days = 8
i = -1
while True:
    i = i + 1
    stream(i)
    if i == max_days:
        i = -1