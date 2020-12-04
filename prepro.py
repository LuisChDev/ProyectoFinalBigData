from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime

analyser = SentimentIntensityAnalyzer()

def readlocal(usr):
    file = open('./data/' + str(usr) + '_cdata.txt', 'r+', encoding='utf-8')
    lines = file.read().splitlines()
    return(lines)

# get XML files
def get_files(master, filedir):
    task_n = sum(1 for x in master)
    task_nc = 0
    dfset = []
    for x in master:
        author = x
        entrydict = build_dict(filedir ,author)
        dfset.append(entrydict)

        datetime_object = str(datetime.datetime.now())
        task_nc += 1
        print('[' + datetime_object + '] finished task ' + str(task_nc) + ' of ' + str(task_n))
    return dfset

def build_dict(filedir ,author):
    file = open("./data/" + filedir + '/' + author + "_tweets.txt", 'r+', encoding='utf-8')
    lines = file.readlines()
    if len(lines) > 0:
        total = len(lines)
    else:
        total = 1  # cero tweets, da igual

    # XML stuff
    #tree = ET.parse(file)
    #root = tree.getroot()

    #NLP stuff

    rts = 0
    links = 0
    punctuation = 0
    hashtags = 0
    tags = 0

    positive = 0
    neutral = 0
    negative = 0
    compound = 0

    #suspicious_words = 0
    #suspicious_words_lsit = ["bot", "bots", "sigueme", "sigame", "seguidores",
    #                         "empleoTIC", "empleoTICJOB", "SEGUIDORES", "SIGUES",
    #                         "Follow", "OBSERVADOR", "DESCARGAR", "ipautaorg", "hacerfotos",
    #                        "Unete", "ccdBot", "VIDEO", "elpaisuy", "ad", "cp", "TrafficBotGT"
    #                        "AJNews", "Venta", "iPhone"]

    for entry in lines:
        text = str(entry)
        text = text.rstrip()

        # suspicious words
        #text_split = entry.text.split()
        #for word in text_split:
        #    if word in suspicious_words_lsit:
        #        suspicious_words += 1

        # Sentiment
        #text_trans = Translator.translate(text=text, src='es', dest='en')
        score = analyser.polarity_scores(text)
        positive += score['pos']
        neutral += score['neu']
        negative += score['neg']
        compound += score['compound']

        # RT
        rts += text.count('RT @')
        # Link
        links += text.count('http://')
        links += text.count('https://')
        # Punct
        punctuation += text.count('. ')
        punctuation += text.count(', ')
        punctuation += text.count('; ')
        # hashtags
        hashtags += text.count('#')
        # tags
        tags += text.count('@')

    entrydict = {
        "author": author,
        "rts": rts/total,
        "links": links/total,
        "punctuation": punctuation/total,
        "hashtags": hashtags/total,
        "tags": tags/total,
        # "botvalue": 0,
        "positive": positive/100,
        "neutral": neutral/100,
        "negative": negative/100,
        "compound": compound/100
        # "suspicious_words": suspicious_words
    }

    return entrydict
