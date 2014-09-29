# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    """
    Command used to populate the database with the channels and news of R7
    website (www.r7.com).
    """

    help = 'Populates the database consuming news feed of R7 website'

    def handle(self, *args, **options):
        from news.crawler import NewsCrawler

        NewsCrawler().execute()
