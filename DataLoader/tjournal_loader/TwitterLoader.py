# -*- coding: utf-8 -*-
__author__ = 'popka'
import twitter
from datetime import datetime
from dateutil import tz
import time

class TwitterLoader:


    def __init__(self):
        CONSUMER_KEY = 'BOuuaMDhNhm6yx0rzqK8bMsbI'
        CONSUMER_SECRET = '3DybJwlkXd2vU6R385yLA8yJblYJltLtwojySD9AVs04ShauZ0'

        ACCESS_TOKEN_KEY = '3712177576-of3jzZ8gNmlPDfPjPyR0Ljw1Ao2IXdTqX9dZGDZ'
        ACCESS_TOKEN_SECRET = 'Ky7iKwByHNXX3UMfuMhv6UgVx2IhjLo3KmwpsBQz35wtG'

        self.api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)
        self._month_dict = {"Jan":"1", "Feb":"2", "Mar":"3", "Apr":"4", "May":"5", "Jun":"6", "Jul":"7", "Aug":"8", "Sep":"9", "Oct":"10", "Nov":"11", "Dec":"12"}

        self._UTC_TIME_ZONE = tz.gettz('Europe/London')
        self._MOSCOW_TIME_ZONE = tz.gettz('Europe/Moscow')
        self._RATE_LIMIT = "[{u'message': u'Rate limit exceeded', u'code': 88}]"

        self._news_uri = "https://tjournal.ru/p/{}"



    def _parse_date(self, date):

        """

        :param date: str, дата в формате твиттера - "Sat Nov 21 17:00:29 +0000 2015"
        :return: str, дата в человеческом, но буржуйском формате, да еще и в Московском часовом поясе
        """
        date_array = date.split(' ')
        month = self._month_dict[date_array[1]]
        day = int(date_array[2])
        time = date_array[3]
        year = date_array[5]

        date = str(year)+"-"+str(month)+"-"+str(day)+" "+time
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        utc_date = date.replace(tzinfo=self._UTC_TIME_ZONE)
        moscow_date = utc_date.astimezone(self._MOSCOW_TIME_ZONE)

        return str(moscow_date).split("+")[0]



    def loadTweetWithLink(self, link, date):
        """

        :param link: str, ключевое слово для поиска, вданном случае - ссылка на письмо
        :param date: str, дата, до которой искать твиты
        :return: список словариков с информацией о УНИКАЛЬНЫХ твитах по запросу link
        """
        set_id = set()
        tweet_list = []
        result = self.api.GetSearch(term=link, until=date, count=100000)
        for res in result:

            tw_id = res.GetId()

            # Если мы уже обрабатывали этот твит - идем дальше
            if tw_id in set_id:
                continue

            retweeted_status = res.GetRetweeted_status()
            # Если это не ретвит
            if retweeted_status is None:
                retweeted_count = res.GetRetweetCount()
                favorite_count = res.GetFavoriteCount()
            else:
                retweeted_count = 0
                favorite_count = 0
            set_id.add(tw_id)

            created_at = res.GetCreatedAt()
            created_at = self._parse_date(created_at)

            # Данные о пользователе
            user = res.GetUser()
            followers_count = user.followers_count
            listed_count = user.listed_count
            friends_count = user.friends_count
            favourites_count = user.favourites_count
            statuses_count = user.statuses_count


            link = link.split("/")[-1]

            tw_dict= {
                    "id": link,
                    "tw_id":tw_id,
                    "retweeted_count": retweeted_count,
                    "favorite_count":favorite_count,
                    "created_at":created_at,
                    "user_followers_count":followers_count,
                    "user_listed_count": listed_count,
                    "user_friends_count":friends_count,
                    "user_favourites_count":favourites_count,
                    "user_statuses_count":statuses_count
                    }

            tweet_list.append(tw_dict)

        return tweet_list

    def _get_next_date(self, date, days):
        """

        :param date: str, дата
        :param days: int, количество дней
        :return: возвращает дату через days-дней после date
        """
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date += datetime.timedelta(days=days)
        return str(date)


    def load_tweets_by_term(self, news_list, days_after_news=2):
        """

        :param news_list: list(str), список словариков с информацией о новости
        :param days_after_news:  int, количество дней после публикации новости, до которой искать
        """
        result_list = []
        for news in news_list:
            try:
                uri = self._news_uri.format(news.id)
                self._get_next_date(news.date, days_after_news)
                tweets = self.loadTweetWithLink(news)
            except twitter.error.TwitterError as ex:
                print str(ex)
                if str(ex) == self._RATE_LIMIT:
                    sleep_time = self.api.GetSleepTime("statuses/user_timeline")
                    print "Спим {} сек.".format(sleep_time)
                    time.sleep(sleep_time+2)
                    tweets = self.loadTweetWithLink(news)

            result_list.append(tweets)



