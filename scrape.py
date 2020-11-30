import time
import tweepy
import csv
import os

# Authenticate to twitter
auth = tweepy.OAuthHandler('E###', 'b###')
auth.set_access_token('1###', 'y###')
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_followers(user_name):
    n = 10
    nx = 0
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True,count=200).pages():
        try:
            followers.extend(page)
            print('page ' + str(nx+1) + ' of ' + str(n))
            nx = nx + 1
            if nx == n:
                return followers
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    print('Done early.')
    return followers


def save_followers_to_csv(user_name, data):
    with open("./data/" + user_name + "_followers.csv", 'w+',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        for profile_data in data:
            profile = []
            profile.append(profile_data._json["screen_name"])
            csv_writer.writerow(profile)


def get_followers_list_file(user_name):
    with open("./data/" + user_name + "_followers.csv", 'r+' ,encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        data = list(filter(None, data))
        # data = tuple(data)

    flattened = []
    for sublist in data:
        for val in sublist:
            flattened.append(val)
    # print(flattened)
    return flattened

def listToString(list):
    # initialize an empty string
    string = ""

    # traverse in the string
    for ele in list:
        string += ele
        string += ' '
        # return string
    return string

def comparison(user1):

    followers1 = get_followers(user1)
    save_followers_to_csv(user1, followers1)

    Data1 = get_followers_list_file(user1)

    return Data1

def exportfolls(data, adj):
    f = open("./data/" + str(adj) + "_log.txt", "a+")
    for x in data:
        f.write(x + "\n")
    f.close()

def exporttwts(data, adj, user):
    f = open("./data/" + str(adj) + "/" + str(user) +"_tweets.txt", "a+", encoding='utf-8')
    for x in data:
        f.write(x + "\n")
    f.close()

def wipeprivs(data):
    data2 = []
    lenlt = len(data)
    lx = 0
    for x in data:
        u = api.get_user(x)
        if u.protected == False:
            print(x + ' not protected (' + str(lx+1) + ' of ' + str(lenlt) + ')')
            if u.statuses_count != 0:
                data2.append(x)
        else:
            print(x + ' protected  (' + str(lx+1) + ' of ' + str(lenlt) + ')')
        lx = lx + 1
    print('Followers cleaned up.')
    return data2

def readfolls(data, adj):
    data2 = []
    n = 0
    data = wipeprivs(data)
    print('Scraping tweets...')
    for x in data:
        try:
            currtwts = scrapetweets(x, n)
            exporttwts(currtwts, adj, x)
            data2.append(x)
            n = n + 1
        except:
            print('Exception. Skipping user ' + str(x))
    return data2

    #f.close()
    #return rdata

def scrapetweets(user, n):
    username = user
    print('Scraping ' + str(user) + ' tweets...' + str(n) + ' done')
    count = 100
    #while True:
    #    try:
            # Creation of query method using parameters
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended', wait_on_rate_limit=True).items(count)
            # Pulling information from tweets iterable object
    tweets_list = [tweet.full_text for tweet in tweets]
    return (tweets_list)
    #    except tweepy.TweepError as e:
    #        print("Going to sleep:", e)
    #        time.sleep(60)
    #print(tweets_list)
    #return(tweets_list)

def readlocal(usr):
    file = open('./data/' + str(usr) + '_cdata.txt', 'r+', encoding='utf-8')
    lines = file.read().splitlines()
    return(lines)

def scrapecomp(arg1):
    u1 = str(arg1)

    if not os.path.exists('./data/' + u1 + '/'):
        os.makedirs('./data/' + u1 + '/')

    cdata = comparison(u1)
    #print(cdata)
    cdata = readfolls(cdata, u1)

    file = open('./data/' + str(arg1) + '_cdata.txt', 'w+', encoding='utf-8')
    for x in cdata:
        file.write(str(x) + '\n')

    return cdata

