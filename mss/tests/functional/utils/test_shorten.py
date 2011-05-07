# -*- coding: utf-8 -*-

from mss.utils.shorten_url import ShortenURL
import string

def test_can_shorter():
    assert string.find(ShortenURL().Shorten("<should-be_text>"), 'http://tinyurl.com/') != -1