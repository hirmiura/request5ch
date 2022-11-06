#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura <https://github.com/hirmiura>
import pytest

from request5ch import Request5ch


def test_init_none():
    req5ch = Request5ch()
    assert req5ch
    assert req5ch.url is None

    req5ch = Request5ch(None)
    assert req5ch
    assert req5ch.url is None

    req5ch = Request5ch("")
    assert req5ch
    assert req5ch.url is None


@pytest.mark.parametrize(
    ("url"),
    [
        ("https://test.5ch.net/test/read.cgi/news4vip"),
        ("https://test.5ch.net/test/read.cgi/news4vip/294691274"),
    ],
)
def test_init_good(url):
    req5ch = Request5ch(url)
    assert req5ch
    assert req5ch.url is not None


@pytest.mark.parametrize(
    ("url"),
    [
        ("afsoif m9qw8vm32mva mf9 vuq34vofmfowie"),
        ("ftps://test.5ch.net/test/read.cgi/news4vip/294691274"),
    ],
)
def test_init_ng(url):
    req5ch = Request5ch(url)
    assert req5ch
