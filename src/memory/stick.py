# -*- coding: utf-8 -*-

from src.profiles import CountryProfile
from src.memory.board import Board
from src.prompts.struct_format import NlAction


class Stick:
    """国家代理专属信息库"""

    def __init__(
            self, country: CountryProfile, countries: list[CountryProfile], board: Board
    ) -> None:
        self.profile = country
        self.name = country.country_name
        self.countries_profile = countries

        self.board = board
        self.mobilization = False

    def get_mob(self) -> bool:
        """获取动员状态"""
        return self.mobilization

    def update(self, actions: list[NlAction]) -> None:
        """更新信息库"""
        for action in actions:
            if action.action == "General Mobilization":
                self.mobilization = True
