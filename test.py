# -*- coding: utf-8 -*-
"""
    Hello, World!
    ~~~~~~~~~~~~~

    An example app showing the basic use of Flask with templates.

    :copyright: (c) 2018 by bmcculley.
    :license: MIT, see LICENSE for more details.
"""

import pytest

import os
import app


@pytest.fixture
def client(request):
    client = app.app.test_client()
    return client

def test_home_page(client):
    rv = client.get('/')
    assert b'Hello, World!' in rv.data
