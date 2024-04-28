# -*- coding: utf-8 -*-

from src.components.country import CountryProfile
from src.components.board import Board
from src.components.enum import CountryRel
from src.history.agent_actions import Action


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

    def get_countries_with_rel(self, rel: CountryRel) -> list[str]:
        """获取特定关系的国家"""
        return [k for k, v in self.rels.items() if v == rel]

    def get_mob(self) -> bool:
        """获取动员状态"""
        return self.mobilization

    def update(self, actions: list[Action]) -> None:
        """更新信息库"""
        for action in actions:
            self.rels[action.target] = action.rel
        self.mobilization = any(action.name == "Mobilization" for action in actions)
