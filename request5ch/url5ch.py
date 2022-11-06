#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura <https://github.com/hirmiura>
import re


class URL5ch:
    DOMAIN_BASE = "5ch.net"
    READ_CGI = "/test/read.cgi"
    BBS_CGI = "/test/bbs.cgi"
    SUBJECT_TXT = "subject.txt"
    re_url = re.compile(
        # fmt:off
        r"(?P<scheme>https?)://"
        r"(?P<host>[^/\.]+)\."
        f"{re.escape(DOMAIN_BASE)}"
        r"/test/read\.cgi/"
        r"(?P<bbs>[^/]+)(/(?P<tid>\d+))?"
        # fmt:on
    )

    def __init__(self, domain_host: str = "", bbs: str = "", tid: str = "") -> None:
        assert domain_host is not None
        assert bbs is not None
        assert tid is not None
        self.scheme = "https"
        self.domain_host = domain_host
        self.bbs = bbs
        self.tid = tid

    @classmethod
    def parse(cls, url: str):
        assert url
        obj = None
        m = URL5ch.re_url.match(url)
        if m:
            scheme = m.group("scheme")
            host = m.group("host")
            bbs = m.group("bbs")
            tid = m.group("tid") or ""
            obj = cls(host, bbs, tid)
            obj.scheme = scheme
        return obj

    @property
    def server(self) -> str:
        result = ""
        if self.domain_host:
            result = "".join((self.domain_host, ".", URL5ch.DOMAIN_BASE))
        return result

    @property
    def server_url(self) -> str:
        result = ""
        server = self.server
        if self.scheme and server:
            result = "".join((self.scheme, "://", server))
        return result

    @property
    def subject_txt_url(self) -> str:
        """subject.txtのURLを返す"""
        result = ""
        server_url = self.server_url
        if server_url and self.bbs:
            result = "".join((server_url, "/", self.bbs, "/", URL5ch.SUBJECT_TXT))
        return result

    @property
    def post_path(self):
        return URL5ch.BBS_CGI

    @property
    def bbs_cgi_url(self) -> str:
        result = ""
        server_url = self.server_url
        if server_url:
            result = "".join((server_url, URL5ch.BBS_CGI))
        return result

    @property
    def thread_url(self) -> str:
        result = ""
        server_url = self.server_url
        if server_url:
            result = "".join((server_url, URL5ch.READ_CGI, "/", self.bbs, "/", self.tid, "/"))
        return result
