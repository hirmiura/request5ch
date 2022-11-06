#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura <https://github.com/hirmiura>
import pytest

from request5ch import URL5ch


def test_url5ch_init_none():
    """Noneでアサートされることを確認する"""

    with pytest.raises(AssertionError) as e:
        url5ch = URL5ch(None)  # type: ignore
    assert e

    with pytest.raises(AssertionError) as e:
        url5ch = URL5ch("", None)  # type: ignore
    assert e

    with pytest.raises(AssertionError) as e:
        url5ch = URL5ch("", "", None)  # type: ignore
    assert e

    with pytest.raises(TypeError) as e:
        url5ch = URL5ch("", "", "", "")  # type: ignore
    assert e

    with pytest.raises(AssertionError) as e:
        url5ch = URL5ch(domain_host=None)  # type: ignore
    assert e

    with pytest.raises(AssertionError) as e:
        url5ch = URL5ch(bbs=None)  # type: ignore
    assert e

    with pytest.raises(AssertionError) as e:
        url5ch = URL5ch(tid=None)  # type: ignore
    assert e


def test_url5ch_init():
    u = URL5ch("host", "news4vip", "294691274")
    assert u
    assert u.scheme == "https"
    assert u.domain_host == "host"
    assert u.bbs == "news4vip"
    assert u.tid == "294691274"
    assert u.server == "host.5ch.net"
    assert u.server_url == "https://host.5ch.net"
    assert u.subject_txt_url == "https://host.5ch.net/news4vip/subject.txt"
    assert u.post_path == "/test/bbs.cgi"
    assert u.bbs_cgi_url == "https://host.5ch.net/test/bbs.cgi"
    assert u.thread_url == "https://host.5ch.net/test/read.cgi/news4vip/294691274/"


def test_url5ch_parse_none():
    with pytest.raises(AssertionError) as e:
        u = URL5ch.parse(None)  # type: ignore
    assert e


@pytest.mark.parametrize(
    ("url"),
    [
        ("ftp://test.5ch.net/hogehoge"),
        ("https://mi.5ch.net/news4vip/"),
        ("afsoif m9qw8vm32mva mf9 vuq34vofmfowie"),
    ],
)
def test_url5ch_parse_invalid(url):
    u = URL5ch.parse(url)
    assert u is None


@pytest.mark.parametrize(
    (
        "url",
        "expected_scheme",
        "expected_host",
        "expected_bbs",
        "expected_tid",
        "expected_server",
        "expected_server_url",
    ),
    [
        (
            "http://mi.5ch.net/test/read.cgi/news4vip/1667481658",
            "http",
            "mi",
            "news4vip",
            "1667481658",
            "mi.5ch.net",
            "http://mi.5ch.net",
        ),
        (
            "http://mi.5ch.net/test/read.cgi/news4vip/1667481658/",
            "http",
            "mi",
            "news4vip",
            "1667481658",
            "mi.5ch.net",
            "http://mi.5ch.net",
        ),
        (
            "http://mi.5ch.net/test/read.cgi/news4vip/1667481658/l50",
            "http",
            "mi",
            "news4vip",
            "1667481658",
            "mi.5ch.net",
            "http://mi.5ch.net",
        ),
        (
            "http://mi.5ch.net/test/read.cgi/news4vip/1667481658/10-420",
            "http",
            "mi",
            "news4vip",
            "1667481658",
            "mi.5ch.net",
            "http://mi.5ch.net",
        ),
        (
            "http://mi.5ch.net/test/read.cgi/news4vip",
            "http",
            "mi",
            "news4vip",
            "",
            "mi.5ch.net",
            "http://mi.5ch.net",
        ),
        (
            "http://mi.5ch.net/test/read.cgi/news4vip/",
            "http",
            "mi",
            "news4vip",
            "",
            "mi.5ch.net",
            "http://mi.5ch.net",
        ),
    ],
)
def test_parse_valid_url(
    url,
    expected_scheme,
    expected_host,
    expected_bbs,
    expected_tid,
    expected_server,
    expected_server_url,
):
    u = URL5ch.parse(url)
    assert u
    assert u.scheme == expected_scheme
    assert u.domain_host == expected_host
    assert u.bbs == expected_bbs
    assert u.tid == expected_tid
    assert u.server == expected_server
    assert u.server_url == expected_server_url
