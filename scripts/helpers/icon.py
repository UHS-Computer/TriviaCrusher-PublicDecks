from uuid import UUID
from typing import List
from datetime import datetime
import json_fix


class Icon:
    fontFamily: str | None
    codePoint: int
    fontFamilyFallback: str | None
    fontPackage: str | None
    matchTextDirection: bool | None

    def __json__(self):
        return self.__dict__

    def __init__(self, font_family: str | None, code_point: int, font_family_fallback: str | None, font_package: str | None, match_text_direction: bool | None) -> None:
        self.fontFamily = font_family
        self.codePoint = code_point
        self.fontFamilyFallback = font_family_fallback
        self.fontPackage = font_package
        self.matchTextDirection = match_text_direction
