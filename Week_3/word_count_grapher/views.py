# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from google.appengine.api import memcache

import logging
import word_counter


class WordCountForm(forms.Form):
    """ This form simply asks for a url to feed to the word counter/grapher """
    url = forms.URLField(required=True)

def word_count_index(request):
    """ This view shows the form """
    form = WordCountForm()
    c = {'form':form}
    return render_to_response('word_count_grapher/word_count_form.html', c)

def word_count_results(request):
    """ This views shows the results of the word count"""
    form = WordCountForm(request.POST)
    c = {}
    if form.is_valid():
        # Get url and find the word counts
        url = form.cleaned_data['url']
        word_counts = word_counter.parse_website(url)

        # Get top 10 highest count words and store in words and
        #   num_occurrences list
        top10 = word_counter.get_top_10(word_counts)
        words = []
        num_occurrences  = []
        for key, val in top10:
            words.append(key)
            num_occurrences.append(val)
        c.update({'words': words})
        c.update({'num_occurrences': num_occurrences})

        # Get shortest and longest words
        c.update({'shortest_word': word_counter.get_shortest_word(word_counts).popitem()[0]})
        c.update({'longest_word': word_counter.get_longest_word(word_counts).popitem()[0]})

    return render_to_response('word_count_grapher/results.html', c)
