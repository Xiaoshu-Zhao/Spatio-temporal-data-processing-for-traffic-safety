import snscrape.modules.twitter as sntwitter
import itertools
import pandas as pd

def search_by_text(text = '#reopen', start = '2020-05-01', end = '2020-06-01', numberOfTweets = 100):
    '''
    the format should be: text, start, end, radius, numberOfTweets
    the default location is new york within 100km.
    text: the search key
    start, end: time constaint
    numberOfTweets: the number of tweets that you want to scrape. 
    '''
    
    scraped_tweets = sntwitter.TwitterSearchScraper(f'{text} since:{start} until:{end} near:"New York"').get_items()
 
    sliced_scraped_tweets = itertools.islice(scraped_tweets, numberOfTweets)
    tweets_df = pd.DataFrame(sliced_scraped_tweets)
    return tweets_df


def search_by_tweet_id(since_id=1320246372008853503, max_id=1320246372008853504, numberOfTweets = 100):
    '''

    '''
    
    scraped_tweets = sntwitter.TwitterSearchScraper(f'since_id:{since_id} max_id:{max_id} filter:safe').get_items()
 
    sliced_scraped_tweets = itertools.islice(scraped_tweets, numberOfTweets)
    tweets_df = pd.DataFrame(sliced_scraped_tweets)
    return tweets_df




def search_by_username(username = 'jack', numberOfTweets = 0):
    '''
    this method could get the demographic information of user
    username: the user that you want to search
    numberOfTweets: the number of tweets that you want to scrape. 
    '''
    
    # Creating list to append tweet data
    tweets_list = []

    # Using TwitterSearchScraper to scrape 100 records from username @jack
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{username}').get_items()):
        if i > numberOfTweets:
            break
        tweets_list.append([tweet.user.username, tweet.user.description, tweet.user.verified, tweet.user.followersCount, tweet.user.location])
    
    tweets_df = pd.DataFrame(tweets_list, columns = ['username', 'description', 'verified', 'followersCount', 'location'])
    
    return tweets_df


def search_by_location(text = '#reopen', 
                       coordinates = '40.730610,-73.935242, 500000mi',
                       start = '2020-03-01',
                       end = '2021-03-31',
                       language = 'en',
                       numberOfTweets = 100):
    '''
    this method could location detail of tweets that include text you want.
    
    '''

    scraped_tweets = sntwitter.TwitterSearchScraper(f'{text} since:{start} until:{end} geocode:"{coordinates}" lang:{language}')\
                                  .get_items()

    sliced_scraped_tweets = itertools.islice(scraped_tweets, numberOfTweets)
    df_coord = pd.DataFrame(sliced_scraped_tweets)[['date', 'user', 'content']]

    # getting user's location
    df_coord['user_location'] = df_coord['user'].apply(lambda x: x['location'])
    
    df_coord['user'] = df_coord['user'].apply(lambda x: x['username'])
    return df_coord[['user', 'date', 'content']]


def search_mention(text = '#reopen',radius = '100km', numberOfTweets = 100):
    '''
    this method could get the dataframe with user and mentioned user
    
    '''
    
    def get_mentioned(row):
        mentions = []
        for item in row:
            mentions.append(item['username'])
        return mentions

    # get 100 tweets with mentions by search data science
    scraped_tweets = sntwitter.TwitterSearchScraper(f'{text} lang:en filter:mentions near:"New York" within:{radius}').get_items()
    sliced_scraped_tweets = itertools.islice(scraped_tweets, numberOfTweets)
    df = pd.DataFrame(sliced_scraped_tweets)[['date', 'content', 'user', 'mentionedUsers']]

    # extract username
    df['user'] = df['user'].apply(lambda x: x['username'])
    # extract mentioned username
    #df['mentionedUsers'] = df['mentionedUsers'].apply(get_mentioned)
    
    return df
    