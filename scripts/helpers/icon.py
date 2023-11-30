from uuid import UUID
from typing import List
from datetime import datetime


class Icon:
    font_family: str | None
    code_point: int
    font_family_fallback: str | None
    font_package: str | None
    match_text_direction: bool | None

    def __init__(self, font_family: str | None, code_point: int, font_family_fallback: str | None, font_package: str | None, match_text_direction: bool | None) -> None:
        self.font_family = font_family
        self.code_point = code_point
        self.font_family_fallback = font_family_fallback
        self.font_package = font_package
        self.match_text_direction = match_text_direction
