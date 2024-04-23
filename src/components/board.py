# -*- coding: utf-8 -*-

from src.components.country import CountryProfile
from src.components.enum import CountryRel


class Board:
    """
    公共信息库

    各个国家当前公开可见的状态以及各个国家间已公开的国际关系
    """

    def __init__(self, countries: list[CountryProfile]) -> None:
        self.country_profiles = countries
        self.country_names = [country.country_name for country in countries]
        # 初始化国家间关系,均为‘-’
        self.country_relations = {
            country: {target: CountryRel.N for target in self.country_names}
            for country in self.country_names
        }

    def get_rel(self, country1: str, country2: str) -> str:
        """获取两个国家间的关系"""
        return self.country_relations[country1][country2]
