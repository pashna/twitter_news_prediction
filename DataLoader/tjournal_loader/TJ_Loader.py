# -*- coding: utf-8 -*-
__author__ = 'popka'
import lxml.html as html
from urllib2 import urlopen


class TJLoader:

    def __init__(self):
        self._news_pages = "https://tjournal.ru/paper/category/news/page/{}"
        self._month_map = {u"января":"01", u"февраля":"02", u"марта":"03", u"апреля":"04", u"мая":"05", u"июня":"06", u"июля":"07", u"августа":"08", u"сентября":"09", u"октября":"10", u"ноября":"11", u"декабря":"12"}

    def get_news_uri(self, min_index=10, count=30):
        """

        :param min_index: int, индекс страницы, с которой нужно начать поиск
        :param count: int, количество страниц, которые нужно скачать
        :return: list. список ссылок на новости
        """
        links = []
        for i in range(count):

            page = html.parse(urlopen(self._news_pages.format(i+min_index)))
            divs = page.getroot().find_class('b-articles__b__title')

            for div in divs:
                links.append(div.getchildren()[1].get("href"))

        return links


    def _parse_date(self, date):
        date = date.replace(",", "")
        date = date.split(" ")

        converted_date = date[2]
        converted_date +="-"+self._month_map[date[1]]
        converted_date +="-"+date[0]

        converted_date +=" "+date[3]

        return converted_date


    def get_link_info(self, link):
        """

        :param link: str, url страницы с tjournal, для которой нужно собрать информацию
        :return: dict с данными со страницы
        """
        page = html.parse(urlopen(link))
        root = page.getroot()

        # заголовок
        title = root.find_class("b-article__title")
        title = title[0].find("h1").text

        # парсим количество просмотров
        view = root.get_element_by_id("hitsCount").text
        view = view.replace(" ", "")
        view = int(view)

        # Количество комментариев
        comments = root.find_class("b-article__infoline__comments")
        comment = int(comments[0].find("b").text.replace(" ", ""))

        # Теги
        tags = root.find_class("b-article__tags__tag")
        tag_list = []
        for tag in tags:
            tag_list.append(tag.text)

        # Дата
        date = root.find_class("b-article__infoline__date")
        date = self._parse_date(date[0].text)


        return {"title": title, "views": view, "comments": comment, "tags": tag_list, "date": date}


    def get_tj_news_info(self, min_index=10, count=30):
        """

        :param min_index: int, индекс страницы, с которой начинаем собирать новости
        :param count: int, количество страниц, с которых соберем новости
        :return: список новостей в формате, возвращаемом функцией get_link_info
        """
        links = self.get_news_uri(min_index=min_index, count=count)
        link_info_list = []
        for link in links:
            link_info = self.get_link_info(link)
            link = link.split("/")[-1]
            link_info["id"] = link
            link_info_list.append(link_info)

        return link_info_list