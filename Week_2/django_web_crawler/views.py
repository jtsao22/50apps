# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from google.appengine.api import memcache
import logging
import web_crawl


class CrawlerForm(forms.Form):
    """ This is a form for crawling a url to a certain depth for a search text """
    url = forms.CharField(required=True)
    depth = forms.IntegerField(min_value=1, max_value=10, required=True)
    search_text = forms.CharField(required=True)

def index(request):
    """ This view shows the form """
    form = CrawlerForm()
    return render_to_response('django_web_crawler/web_crawler_form.html', {'form': form})

def results(request):
    """ This views shows the results of the crawl """
    form = CrawlerForm(request.POST)
    if form.is_valid():
        url = form.cleaned_data['url']
        depth = form.cleaned_data['depth']
        search_text = form.cleaned_data['search_text']
        urls_with_search_text = []

        logging.info("URL: " + str(url))
        logging.info("DEPTH: " + str(depth))
        logging.info("SEARCH_TEXT:  " + search_text)

        #url = 'http://jtsao22.wordpress.com'
        #depth = 1
        #search_text = 'Open'

        web_crawl.find_urls_with_search_text(str(url), depth, search_text, urls_with_search_text);
    return render_to_response('django_web_crawler/results.html', {'data': urls_with_search_text})
