import tweepy
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd


#Credentials
consumer_key = "xxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxx"
access_key = "xxxx-xxxxxxxxxxxxxxxx"
access_secret = "xxxxxxxxxxxxxxxxxxxx"



tweet_id_list = []
# Function to extract tweets
def get_tweets(username):
    with open("C:\\xxxxxxxxxx\id.txt", 'r') as myfile: #get the status id from previous run
        latest_id = myfile.read().strip()
        myfile.close()

    print (latest_id)

    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Calling api
    api = tweepy.API(auth)

    # 200 tweets to be extracted
    number_of_tweets = 3000

    #tweets = api.user_timeline(screen_name=username, count=number_of_tweets,tweet_mode="extended")
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, since_id=latest_id,count=number_of_tweets,tweet_mode="extended").items():
        if 'enter_your_search_string' in tweet.full_text: #status id's are extracted for our search string mentioned within quotes
            print(tweet.full_text)
            print(tweet.id)
            tweet_id_list.append(tweet.id)



#intializing the variables to extract the tweets
question=[]
answer=[]

#function to scrap the whole conversation
def scraping(id):

    url='https://twitter.com/user_id/status/'+str(id)
    print(url)

    response=req.get(url)
    contents=bs(response.content, 'html.parser')

    content_count = 0
    for i in contents.find_all(class_='TweetTextSize'):
        content_count += 1

    if content_count == 2:
        counter=0
        for i in contents.find_all(class_='TweetTextSize'):
            if counter==0:
                print (question.append(i.get_text()))
            elif counter==1:
                print(answer.append(i.get_text()))

            counter+=1




# Driver code
if __name__ == '__main__':
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    get_tweets("user_id")

    for n in tweet_id_list:
        scraping(n)

    #Writing the arrays results into excel file
    tweep = "C:\\xxxxxxxxxxxxxxxx\\tweet.xlsx"
    df3 = pd.DataFrame.from_dict({'Questions': question, 'Answers': answer})
    df3.to_excel(tweep, header=True, index=False)

    #Updating the file with max_id which will be used as latest_id in next run
    if len(tweet_id_list) > 0:
        with open("C:\\xxxxxxxxxxxxxxxx\\id.txt", 'w') as myfile2:
            myfile2.write(str(tweet_id_list[0]))
            myfile2.close()
    else:
        print("No new entries")



