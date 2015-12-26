import pandas as pd
from datetime import datetime, timedelta


class DataAggregator:

    def __init__(self, news_file, tweets_file):
        self._prepare(news_file, tweets_file)


    def _prepare(self, news_file, tweets_file):
        """
        Функция считывает данные и производит с ними общие преобразования. Вычисляет:
        1) количество минут с момента публикации записи до данного твита
        2) номер дня недели новости
        3) время с полуночи новости

        :param news_file: путь к файлу с новостями
        :param tweets_file: путь к файлу с твиттами
        """
        # Считываем и мерджим данные
        news_info = pd.read_csv(news_file, sep=",")
        tweeter_data = pd.read_csv(tweets_file, sep=",")
        self.df = news_info.merge(tweeter_data, on='url', left_index=True, right_index=False)

        # Общие преобразования
        self._general_apply()

        # Фильтруем новости с ошибочной датой и удаляем очень ранние и очень поздние
        self._filter_news()


    def _general_apply(self):

        """
        Проводит общие преобразования, не зависящие от FirstTime и LastTime
        :return:
        """

        def diff_date_minutes(news_date, tweet_date):
            news_date = datetime.strptime(news_date, '%Y-%m-%d %H:%M')
            tweet_date = datetime.strptime(tweet_date, '%Y-%m-%d %H:%M:%S')
            return int((tweet_date-news_date).total_seconds()/60)

        def get_week_day(date):
            date = datetime.strptime(date, '%Y-%m-%d %H:%M')
            return date.weekday()

        def get_minutes_since_midnight(date):
            midnight = date.split(" ")[0] + " 00:00"
            date = datetime.strptime(date, '%Y-%m-%d %H:%M')
            midnight = datetime.strptime(midnight, '%Y-%m-%d %H:%M')
            return int((date-midnight).total_seconds()/60)


        self.df["time_since_news"] = self.df.apply(lambda s: diff_date_minutes(s["news_date"], s["created_at"]), axis=1)
        self.df["week_day_news"] = self.df.news_date.apply(lambda s: get_week_day(s))
        self.df["minutes_since_midnight"] = self.df.news_date.apply(lambda s: get_minutes_since_midnight(s))



    def _get_hours_before(self, date, hours=3):
            """
            "Перевод часов"
            Функция возвращает дату-строку, за hours часов до даты date
            Если нужно перевести стрелки часов вперед - передаем со знаком минус
            :param date:
            :param hours:
            :return:
            """
            date = datetime.strptime(date, '%Y-%m-%d %H:%M')
            d = date - timedelta(hours=hours)
            d = str(d).split(":")
            d = d[0]+":"+d[1]
            return d


    def _filter_news(self):

        # Есть новости с ошибочной датой. Их исключаем
        self.df = self.df[self.df["time_since_news"] > 0]

        # Отсечем новости в первые и в последние n_hours часов
        n_hours = 8
        max_date = self.df.news_date.max()
        min_date = self.df.news_date.max()

        first_date =  self._get_hours_before(min_date, -n_hours)
        last_date = self._get_hours_before(max_date, n_hours)

        self.df = self.df[self.df["news_date"] > first_date]
        self.df = self.df[self.df["news_date"] < last_date]










