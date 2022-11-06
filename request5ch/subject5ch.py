#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura <https://github.com/hirmiura>
import dataclasses
import io
import re
from typing import Optional


@dataclasses.dataclass
class SubjectItem:
    tid: str
    title: str
    resnum: int


class Subject5ch:
    """subject.txtの内容を保持するクラス"""

    re_parse = re.compile(r"^(?P<tid>\d+)\.dat<>(?P<title>.+)  ?\((?P<resnum>\d+)\)\r?\n?$")

    def __init__(self, url: Optional[str] = None) -> None:
        self.url = url
        self._total_count = 0
        self._threads: list[SubjectItem] = []

    @property
    def total_count(self) -> int:
        """スレの総数"""
        return self._total_count

    @property
    def threads(self) -> list[SubjectItem]:
        return self._threads

    @classmethod
    def parse(cls, text: str):
        assert text
        li = []

        with io.StringIO(text) as f:
            fli = f.readlines()
            for item in fli:
                m = Subject5ch.re_parse.match(item)
                if m:
                    tid = m.group("tid")
                    title = m.group("title")
                    resnum = int(m.group("resnum"))
                    li.append(SubjectItem(tid, title, resnum))
        sbj = cls()
        sbj._threads = li
        sbj._total_count = len(li)
        return sbj

    def search(self, tid) -> Optional[SubjectItem]:
        """tidからスレを検索する

        Args:
            tid: スレのID

        Returns:
            SubjectItem型のスレ情報を返す。見つからなければNoneを返す。
        """
        assert tid
        item = next((th for th in self._threads if th.tid == tid), None)
        return item

    def search_index(self, tid: str) -> Optional[int]:
        """tidからスレのインデックスを検索する

        Args:
            tid: スレのID

        Returns:
            リストのインデックスを返す。見つからなければNoneを返す。
        """
        assert tid
        item = self.search(tid)
        if item:
            return self._threads.index(item)
        else:
            return None

    def search_title(self, tid: str) -> str:
        """tidからスレタイを検索する

        Args:
            tid: スレのID

        Returns:
            スレタイを返す。見つからなければ空文字列を返す。
        """
        assert tid
        item = self.search(tid)
        if item:
            return item.title
        else:
            return ""

    def search_resnum(self, tid: str) -> Optional[int]:
        """tidからレス数を検索する

        Args:
            tid: スレのID

        Returns:
            レス数を返す。見つからなければNoneを返す。
        """
        assert tid
        item = self.search(tid)
        if item:
            return item.resnum
        else:
            return None

    def search_tuple(self, tid) -> Optional[tuple[int, str, int]]:
        """tidからスレ情報を検索する

        Args:
            tid: スレのID

        Returns:
            インデックス、タイトル、レス数をタプルで返す。
            見つからなければNoneを返す。
        """
        assert tid
        item = self.search(tid)
        if item:
            index = self._threads.index(item)
            title = item.title
            resnum = item.resnum
            return (index, title, resnum)
        else:
            return None
