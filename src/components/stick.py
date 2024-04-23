# -*- coding: utf-8 -*-

from src.components.country import CountryProfile
from src.components.board import Board
from src.components.enum import CountryRel


class Stick:
    """国家代理专属信息库"""

    def __init__(
        self, country: CountryProfile, countries: list[CountryProfile], board: Board
    ) -> None:
        self.profile = country
        self.name = country.country_name
        self.countries_profile = countries
        self.countries_name = [c.name for c in countries if c is not country]

        self.board = board
        self.mobilization = False
        self.rels = {n: CountryRel.N for n in self.countries_name}

    def get_rel(self, country: str) -> str:
        """获取国家间关系"""
        return self.rels[country]

    def get_mob(self) -> bool:
        """获取动员状态"""
        return self.mobilization
