# -*- coding: utf-8 -*-
__author__ = 'popka'
import twitter
from tjournal_loader.TJ_Loader import TJLoader
from tjournal_loader.TwitterLoader import TwitterLoader


"""
CONSUMER_KEY = 'BOuuaMDhNhm6yx0rzqK8bMsbI'
CONSUMER_SECRET = '3DybJwlkXd2vU6R385yLA8yJblYJltLtwojySD9AVs04ShauZ0'

ACCESS_TOKEN_KEY = '3712177576-of3jzZ8gNmlPDfPjPyR0Ljw1Ao2IXdTqX9dZGDZ'
ACCESS_TOKEN_SECRET = 'Ky7iKwByHNXX3UMfuMhv6UgVx2IhjLo3KmwpsBQz35wtG'

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

result = api.GetSearch(term="https://tjournal.ru/p/windows-30", until="2015-11-22", count=10000)

set_id = set()

for res in result:

    tw_id = res.GetId()

    # Если мы уже обрабатывали этот твит - идем дальше
    if tw_id in set_id:
        continue

    retweeted_status = res.GetRetweeted_status()
    # Если это не ретвит
    if retweeted_status is None:
        retweeted = res.GetRetweetCount()
        favorite_count = res.GetFavoriteCount()
    else:
        retweeted = 0
        favorite_count = 0
    set_id.add(tw_id)

    res.GetCreatedAt()

    user = res.GetUser()
    followers_count = user.followers_count
    listed_count = user.listed_count
    friends_count = user.friends_count
    favourites_count = user.favourites_count
    statuses_count = user.statuses_count


    print followers_count
"""
"""
for i in result[:4]:
    print str(i)
"""
"""
print result[0].GetFavoriteCount()
print str(result[0])

print result[4].GetFavoriteCount()
print str(result[4])
"""


tw = TwitterLoader()
tj = TJLoader()

news_list = tj.get_news_uri()
