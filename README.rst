========================
opps-news-demo
========================

Opps demo application for news website.

Basically it is a simple project that uses opps.comments and has a crawler that catch the channels and news from the RSS of www.r7.com website.

The crawler runs for a task of celery every 3 minutes.

Dependencies
============

    sudo apt-get install python-dev

    sudo apt-get install python-virtualenv

    sudo apt-get install redis-server


Installation
============

    git clone https://github.com/ervilis/opps-news-demo.git oppsnews

    virtualenv venv

    source venv/bin/activate

    pip install -r oppsnews/requirements.txt

    python oppsnews/manage.py syncdb --noinput

    python oppsnews/manage.py migrate

    python oppsnews/manage.py createsuperuser


Run
===

Celery worker:

    python oppsnews/manage.py celery worker --loglevel=error --events --beat

Webserver

    python oppsnews/manage.py runserver