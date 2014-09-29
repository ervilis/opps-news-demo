# -*- encoding: utf-8 -*-
from django.utils import timezone
from celery import task


@task.periodic_task(run_every=timezone.timedelta(minutes=3))
def update_news():
    from news.crawler import NewsCrawler

    NewsCrawler().execute()
