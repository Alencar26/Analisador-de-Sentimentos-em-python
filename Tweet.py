from textblob import TextBlob
from googletrans import Translator
from unidecode import unidecode
import sys, tweepy
import matplotlib.pyplot as plt


def percentage(part, whole):
    return 100 * float(part)/float(whole)

# ESSAS KEYs SÃO FORNECIDAS PELO TWITTER PARA QUEM TEM CONTA DE DEV.  
consumerKey = 'KEY AQUI'
consumerSecret = 'KEY AQUI'
accessToken = 'KEY AQUI'
accessTokenSecret = 'KEY AQUI'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

searchTerm = input("Digite Palavra-chave/Tag para pesquisar: ")
noOfSearchTerms = int(input("Digite quantos tweets deseja pesquisar: "))
titulo = searchTerm
searchTerm = searchTerm + "-filter:retweets"
tweets = tweepy.Cursor(api.search, q=searchTerm, lang="pt").items(noOfSearchTerms)

positive = 0
negative = 0
neutral = 0
polarity = 0

for tweet in tweets: 
    textEN = Translator().translate(unidecode(tweet.text))
    print("[pt]"+ tweet.text)
    print("[en]"+textEN.text)
    print("\n")
    analysis = TextBlob(textEN.text)
    polarity += analysis.sentiment.polarity

    if (analysis.sentiment.polarity == 0):
        neutral += 1
    elif (analysis.sentiment.polarity < 0.00):
        negative += 1
    elif (analysis.sentiment.polarity > 0.00):
        positive += 1    

positive = percentage(positive, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)

positive = format(positive, '.2f')
neutral = format(neutral, '.2f')
negative = format(negative, '.2f')

print("Como as pessoas estão reagindo a " + titulo + "." + " Foram analisados " + str(noOfSearchTerms) + " tweets.")

if (polarity == 0):
    print("Neutral")
elif(polarity < 0):
    print("Negative")
elif(polarity > 0):
    print("Positive")


labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+ str(neutral) +'%]' , 'Negative ['+ str(negative) +'%]']
sizes = [positive , neutral , negative]
colors = ['yellowgreen' , 'gold' , 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title('Como as pessoas estão reagindo a ' + titulo + "."+ '  Foram analisados ' + str(noOfSearchTerms) + ' tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()