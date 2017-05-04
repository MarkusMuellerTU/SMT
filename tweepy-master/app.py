# -*- coding: utf-8 -*-
"""
Spyder Editor

SMT-Ass2: Differences in nutrition habits between Austria/Germany and the USA
@author: Markus Müller
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

ckey = 'S3q10QInGFuQcvYRgNJx5AZWD'
csecret = 'A9QN45woZVJewCZykYbbrYArVZ3oppVlCXax6srF1zKCqbVsjx'
atoken = '3865326437-emzK4kEVZXixi95VrxuAiCLXFICKzziSR59ORxp'
asecret = 'vJUWdWjPJpz5uX1aL2wynnbbD2er3lrKc0iDnpJEBAmPn'

class listener(StreamListener):
    def on_data(self, data):
        try:
            #print (data)
            
            tweet = data.split(',"text":"')[1].split('"source')[0]
            #print (tweet)
            
            saveThis = str(time.time())+'::'+tweet
            print (saveThis)
            
            saveFile = open('twitDB3.txt', 'a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
            return True
        except BaseException as e:
            print ('failed ondata', str(e))
            time.sleep(5)
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#food", "#foodporn"])