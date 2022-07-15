import re
import pandas as pd
import tweepy

f = open("positive-words.txt", "r")
positivelist = f.read().split()
f.close()
f = open("negative-words.txt", "r")
negativelist = f.read().split()
f.close()
f = open("conjunctive-words.txt", "r")
conj = f.read()
f.close()

api_key = ""
api_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

print("Enter Twitter HashTag to search for:")
hashtag = input()
print("Enter Date since The Tweets are required in dd-mm-yyyy:")
date_since = input()
numtweet = 1000

tweets = tweepy.Cursor(api.search_tweets, hashtag, lang="en", since_id=date_since, tweet_mode='extended').items(numtweet)

sentlist = []

list_tweets = [tweet for tweet in tweets]
for tweet in list_tweets:
    try:
        text = str(ascii(tweet.retweeted_status.get("full_text")))
    except AttributeError:
        text = str(ascii(tweet._json["full_text"]))
    sentlist.append(text)

print('Scraping has completed!')
print('There are '+str(len(list_tweets))+" total tweets scraped!")

scorelist = []
score = 0

sentl = []
prior = ""
atstatus = 1
flipstatus = 1
fliplist = ["aren't", "wasn't", "didn't", "no", "isn't", "ain't", "shouldn't", "couldn't", "none", "can't",
            "won't", "doesn't", "not", "hasn't", "don't"]

for lines in sentlist:
    score = 0
    flipstatus = 1
    sentences = lines.split()
    atstatus = 1
    for words in sentences:
        f=filter(str.isalpha,words)
        words="".join(f)
        if prior in fliplist:
            flipstatus = flipstatus * -1
                    
        if words.lower() in positivelist:
            if prior == "no":
                score -= 1 * atstatus
            else:
                score += 1 * atstatus * flipstatus
                flipstatus = 1
                
        if words.lower() in negativelist:
                score -= 1 * atstatus * flipstatus
                flipstatus = 1

        if words.lower() == "at":
            if prior in positivelist:
                atstatus = 2
            if prior in negativelist:
                atstatus = -2

        prior = words.lower()
    if flipstatus == -1:
        score = -(score*2+1)
    scorelist.append(score)

positives = 0
negatives = 0
neutrals = 0
overall = ""
for ind in range(len(scorelist)):
    if scorelist[ind] >0:
        positives += 1
    if scorelist[ind] <0:
        negatives += 1
    if scorelist[ind] ==0:
        neutrals += 1

if positives > negatives:
    overall = "positive"
elif negatives > positives:
    overall = "negative"
else:
    overall = "neutral"

print("There are positives: " + str(positives) + " negatives: " + str(negatives) + " neutrals: " + str(neutrals)+"\n")
print("Overall tone is " + overall)

    
    

