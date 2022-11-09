#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura <https://github.com/hirmiura>
from datetime import datetime, timedelta, timezone
from logging import getLogger
from typing import Optional, Union

import requests

from .subject5ch import Subject5ch
from .url5ch import URL5ch

logger = getLogger(__name__)
JST = timezone(timedelta(hours=+9), "JST")
SJIS = "cp932"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
ACCEPT_LANGUAGE = "ja,en-US;q=0.7,en;q=0.3"
ACCEPT_ENCODING = "gzip, deflate, br"


class Request5ch:
    TIMEOUT = (6.0, 6.0)

    def __init__(self, url: Optional[str] = None) -> None:
        self.url = URL5ch.parse(url) if url else None

    def set_url(self, url: str) -> bool:
        self.url = URL5ch.parse(url)
        return self.url is not None

    def _create_data_for_post(self, mes: str, name: str, mail: str) -> dict[str, Union[str, bytes]]:
        assert mes is not None
        assert mes != ""
        assert name is not None
        assert mail is not None
        assert self.url
        url = self.url
        data = {
            "FROM": name.encode(SJIS),
            "mail": mail.encode(SJIS),
            "MESSAGE": mes.encode(SJIS),
            "bbs": url.bbs,
            "key": url.tid,
            "time": str(int(datetime.now(JST).timestamp())),
            "submit": "書き込む".encode(SJIS),
            "oekaki_thread1": "",
        }
        return data

    def _create_header_for_post(self) -> dict[str, str]:
        assert self.url
        url = self.url
        headers = {
            "method": "POST",
            "host": url.server,
            "user-agent": USER_AGENT,
            "path": url.post_path,
            "scheme": url.scheme,
            "accept": ACCEPT,
            "accept-language": ACCEPT_LANGUAGE,
            "accept-encoding": ACCEPT_ENCODING,
            "content-type": "application/x-www-form-urlencoded",
            "origin": url.server_url,
            "connection": "close",
            "referer": url.thread_url,
        }
        return headers

    def _create_cookie_for_post(self) -> dict[str, str]:
        cookies = {"yuki": "akari", "READJS": '"off"'}
        return cookies

    def post(self, message: str, name: str = "", mail: str = "") -> requests.Response:
        """投稿する"""
        assert message is not None
        assert message != ""
        assert name is not None
        assert mail is not None
        assert self.url
        url = self.url
        data = self._create_data_for_post(message, name, mail)
        headers = self._create_header_for_post()
        cookies = self._create_cookie_for_post()
        logger.debug("スレ({0}/{1}/{2})に投稿しています".format(url.domain_host, url.bbs, url.tid))
        r = requests.post(
            url.bbs_cgi_url, data=data, headers=headers, cookies=cookies, timeout=Request5ch.TIMEOUT
        )
        logger.debug("スレ({0}/{1}/{2})に投稿しました".format(url.domain_host, url.bbs, url.tid))
        r.encoding = SJIS
        return r

    def _create_header_for_get(self) -> dict[str, str]:
        headers = {
            "user-agent": USER_AGENT,
            "accept": ACCEPT,
            "accept-language": ACCEPT_LANGUAGE,
            "accept-encoding": ACCEPT_ENCODING,
            "connection": "close",
        }
        return headers

    def get_subject(self) -> tuple[Optional[Subject5ch], requests.Response]:
        """subject.txtを取得してSubject5chオブジェクトにして返す"""
        assert self.url
        url = self.url
        headers = self._create_header_for_get()
        logger.debug("subject.txtを取得しています")
        r = requests.get(url.subject_txt_url, headers=headers, timeout=Request5ch.TIMEOUT)
        logger.debug("subject.txtを取得しました")
        r.encoding = SJIS
        sbj = None
        if r.ok:
            sbj = Subject5ch.parse(r.text)
            sbj.url = url.subject_txt_url
        return sbj, r

    def get_thread(self, addition: str = "") -> requests.Response:
        """スレを取得する"""
        assert addition is not None
        assert self.url
        url = self.url
        requrl = url.thread_url + addition
        headers = self._create_header_for_get()
        logger.debug("スレ({0}/{1}/{2})を取得しています".format(url.domain_host, url.bbs, url.tid))
        r = requests.get(requrl, headers=headers, timeout=Request5ch.TIMEOUT)
        logger.debug("スレ({0}/{1}/{2})を取得しました".format(url.domain_host, url.bbs, url.tid))
        r.encoding = SJIS
        return r

    def get_thread_l1(self) -> requests.Response:
        """l1を付けてスレを取得する"""
        return self.get_thread("l1")
