# -*- coding:utf-8 -*-
import re

from django.utils.text import slugify
from django.db.models import get_model


class NewsCrawler(object):

    """
    Class used to populate the database with the channels and news of R7
    website (www.r7.com).
    """

    # URL that has the categories and subcategories available
    rss_url = 'http://www.r7.com/institucional/rss/'

    # User that will be linked to the objects
    _user = None

    def execute(self):
        import requests
        from BeautifulSoup import BeautifulSoup

        User = get_model('auth', 'User')

        # Catch the first user of the database, probably superuser
        self._user = User.objects.all()[0]

        response = requests.get(self.rss_url)
        parser = BeautifulSoup(response.content)

        channels = parser.findAll(
            'div', {'class': re.compile('rss_.*')})

        self._populate_channels(channels)
        self._set_homepage_channel()

    def _populate_channels(self, channels):
        """
        Access the rss page and catch all available channels
        """
        Channel = get_model('channels', 'Channel')

        for parser_chanel in channels:
            name = parser_chanel.find('h6').text
            channel, created = Channel.objects.get_or_create(
                name=name,
                slug=slugify(name),
                show_in_menu=True,
                published=True,
                user=self._user
            )

            # Catch the sub-channels
            sub_channels = parser_chanel.findAll(
                'a', {'href': re.compile('^(?!(#))')})

            for parser_sub_chanel in sub_channels:
                name = parser_sub_chanel.text
                sub_channel, created = Channel.objects.get_or_create(
                    name=name,
                    slug=slugify(name),
                    show_in_menu=True,
                    published=True,
                    user=self._user,
                    parent=channel
                )
                self._populate_posts(sub_channel, parser_sub_chanel['href'])

    def _populate_posts(self, channel, url):
        """
        Get all records from 'feed' and registers the Posts relating them to
        the channel.
        """
        import feedparser

        Post = get_model('articles', 'Post')
        Image = get_model('images', 'Image')

        parser = feedparser.parse(url)

        for entry in parser['entries']:
            # Some entries are incomplete and have only the title, need to
            # ignore these entries.
            if not entry.get('summary'):
                continue

            # The title may have only 140 characters
            title = self._truncate_string(entry['title'], 140)
            slug = slugify(title)
            headline = entry['summary']

            # Some entries do not have the 'content' field, in this case we
            # get the 'summary' field instead.
            if entry.get('content'):
                content = entry['content'][0]['value']
            else:
                content = entry['summary']

            # When we find a entry that already is registered we don't need
            # continue because the following registries already be registered.
            exists = Post.objects.filter(slug=slug).count()
            if exists:
                break

            # Check if has some image in the post content.
            # NOTE: For the best user experience we use only the posts that
            # have images.
            image_url = self._get_image_url_in_content(content)
            if image_url:
                main_image = Image.objects.create(
                    title=title,
                    slug=slug,
                    archive_link=image_url,
                    published=True,
                    user=self._user
                )
                # Generate the 'short_title' based on 'content'
                short_title = re.sub('<[^<]+?>', '', content).encode('utf-8')
                short_title = self._truncate_string(short_title.strip(), 140)

                post = Post.objects.create(
                    title=title,
                    short_title=short_title,
                    slug=slug,
                    headline=headline,
                    content=content,
                    channel=channel,
                    main_image=main_image,
                    show_on_root_channel=True,
                    published=True,
                    hat='',
                    user=self._user
                )

    def _get_image_url_in_content(self, content):
        """
        Grab the first image in the post content
        """
        begin_token = 'src="'
        begin = content.find(begin_token)
        if begin == -1:
            return None

        # Acrescentamos o tamanho do 'begin_token' no 'begin'
        begin += len(begin_token)
        end = content.find('"', begin)
        url = content[begin:end]
        return url.split('?')[0]

    def _set_homepage_channel(self):
        """
        Get the first registered channel and set 'homepage' attribute
        """
        Channel = get_model('channels', 'Channel')

        channel = Channel.objects.all()[0]
        channel.homepage = True
        channel.save()

    def _truncate_string(self, text, max_size):
        """
        Truncate a string in the maximum size usable
        """
        import textwrap

        if len(text) <= max_size:
            return text
        return textwrap.wrap(text, max_size-3)[0] + "..."
