import re
from re import Match
from typing import Callable, Optional

from common.http.request import HTTPRequest
from common.http.response import HTTPResponse

"""
pathがURLパターンにマッチするか判定する
マッチした場合はMatchオブジェクトを返し、マッチしなかった場合はNoneを返す
"""
class URLPattern:
    pattern: str
    view: Callable[[HTTPRequest], HTTPResponse]

    def __init__(self, pattern: str, view: Callable[[HTTPRequest], HTTPResponse]):
        self.pattern = pattern
        self.view = view

    def match(self, path: str) -> Optional[Match]:
        # URLパターンを正規表現パターンに変換する
        # ex) '/user/<user_id>/profile' => '/user/(?P<user_id>[^/]+)/profile'
        pattern = re.sub(r"<(.+?)>", r"(?P<\1>[^/]+)", self.pattern)
        return re.match(pattern, path)