# Stolen from: http://djangosnippets.org/snippets/852/
from django import template
import feedparser

register = template.Library()

class RssParserNode(template.Node):
    def __init__(self, var_name, url=None, url_var_name=None):
        self.url = url
        self.url_var_name = url_var_name
        self.var_name = var_name

    def render(self, context):
        if self.url:
            context[self.var_name] = feedparser.parse(self.url)
        else:
            try:
                context[self.var_name] = feedparser.parse(context[self.url_var_name])
            except KeyError:
                raise template.TemplateSyntaxError, "the variable \"%s\" can't be found in the context" % self.url_var_name
        return ''

import re

@register.tag(name="get_rss")
def get_rss(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    url, var_name = m.groups()
    
    if url[0] == url[-1] and url[0] in ('"', "'"):
        return RssParserNode(var_name, url=url[1:-1])
    else:
        return RssParserNode(var_name, url_var_name=url)
######### End stolen #############

# Stolen from: http://djangosnippets.org/snippets/384/
import urllib, os, time, datetime, feedparser
CACHE_FOLDER = '/path/to/cache/'

@register.inclusion_tag('my_template.html')
def pull_feed(feed_url, posts_to_show=5, cache_expires=30):
    CACHE_FILE = ''.join([CACHE_FOLDER, template.defaultfilters.slugify(feed_url), '.cache'])
    try:
        cache_age = os.stat(CACHE_FILE)[8]
    except: #if file doesn't exist, make sure it gets created
        cache_age = 0
    #is cache expired? default 30 minutes (30*60)
    if (cache_age + cache_expires*60 < time.time()):
        try: #refresh cache
            urllib.urlretrieve(feed_url,CACHE_FILE)
        except IOError: #if downloading fails, proceed using cached file
            pass
    #load feed from cache
    feed = feedparser.parse(open(CACHE_FILE))
    posts = []
    for i in range(posts_to_show):
        pub_date = feed['entries'][i].updated_parsed
        published = datetime.date(pub_date[0], pub_date[1], pub_date[2] )
        posts.append({
            'title': feed['entries'][i].title,
            'summary': feed['entries'][i].summary,
            'link': feed['entries'][i].link,
            'date': published,
        })
    return {'posts': posts}
##### end stolen #############33

