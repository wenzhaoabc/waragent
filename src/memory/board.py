# -*- coding: utf-8 -*-

from src.profiles import CountryProfile
from src.memory.country_rel import CountryRel
from src.prompts.struct_format import NlAction


class Board:
    """
    公共信息库

    各个国家当前公开可见的状态以及各个国家间已公开的国际关系
    """

    def __init__(self, countries: list[CountryProfile]) -> None:
        self.country_profiles = countries
        self.country_names = [country.country_name for country in countries]
        # 初始化国家间关系,均为‘-’，公共可见的关系，所有国家可知
        self.country_relations = {
            country: {
                target: CountryRel.N
                for target in self.country_names
                if country != target
            }
            for country in self.country_names
        }

        # 初始化国家间关系，均为‘-’，私密关系，只有己方国家知道
        self.country_relations_private = {
            country: {
                target: CountryRel.N
                for target in self.country_names
                if country != target
            }
            for country in self.country_names
        }

        # dict[str, dict[str, list[Action]]]
        # 每一轮次，每个国家对其他国家的动作
        self.country_actions = {
            country: {target: [] for target in self.country_names if country != target}
            for country in self.country_names
        }

        self.history = list[list[NlAction]]()

    def get_rel_pub(self, country1: str, country2: str) -> CountryRel:
        """
        获取两个国家间的关系，公共关系
        Args:
            country1: 国家1
            country2: 国家2
        """
        return self.country_relations[country2][country1]

    def get_rel_pri(self, country1: str, country2: str) -> CountryRel:
        """
        获取两个国家间的关系，私密关系
        Args:
            country1: 国家1
            country2: 国家2
        """
        return self.country_relations_private[country2][country1]

    def get_countries_with_rel_pub(self, country: str, rel: CountryRel) -> list[str]:
        """获取与某国家有特定关系的国家"""
        return [
            target
            for target, relation in self.country_relations[country].items()
            if relation == rel
        ]

    def get_countries_with_rel_pri(self, country: str, rel: CountryRel) -> list[str]:
        """获取与某国家有特定关系的国家,本国家私密关系"""
        return [
            target
            for target, relation in self.country_relations_private[country].items()
            if relation == rel
        ]

    def get_countries_with_rel_pub(self, country: str, rel: CountryRel) -> list[str]:
        """获取与某国家有特定关系的国家,公共关系"""
        return [
            target
            for target, relation in self.country_relations[country].items()
            if relation == rel
        ]

    def get_past_history(self, round_time: int = None) -> str:
        """
        获取过去某一轮次的所有国家动作
        """
        history_text = ""
        for index, acs in enumerate(self.history):
            history_text += (
                f"In No {index + 1} day:" + "\n".join([ac.message for ac in acs]) + "\n"
            )

        return history_text

    def get_country_requests(self, country: str) -> list[NlAction]:
        """
        获取某国家的最新的所有请求
        Args:
            country: 国家名
        """
        action_requests = []
        # 过滤出最近的请求
        for round_history in self.history[::-1]:
            added = False
            for ac in round_history:
                # TAG : 请求型动作
                if ac.target == country and (
                    "Request " in ac.action or "Send " in ac.action
                ):
                    if ac.source in [ar.source for ar in action_requests]:
                        continue
                    action_requests.append(ac)
                    added = True
            if not added:
                break

        return action_requests

    def update(self, messages: list[NlAction], round_time: int) -> None:
        """
        更新信息库
        Args:
            messages: 本轮次所有国家的动作
            round_time: 当前轮次
        """
        # 记录历史
        self.history.append(messages)

        # 更新国家间动作记录表
        for message in messages:
            source_country = message.source
            target_country = message.target
            action = message.action
            action_message = message.message

            # 更新国家动作记录表
            self.country_actions[source_country][target_country].append(
                (action, action_message)
            )

        # 本轮两国之间没有互动的，设为默认
        for country in self.country_names:
            for target in self.country_names:
                if (
                    country != target
                    and len(self.country_actions[country][target]) < round_time
                ):
                    self.country_actions[country][target].append(("", "No action"))

        # 更新两国之间的关系
        for message in messages:
            source_country = message.source
            target_country = message.target
            action = message.action
            # 两国之间升级为war
            if action == "Declare War":
                self.country_relations[source_country][target_country] = CountryRel.W
                self.country_relations[target_country][source_country] = CountryRel.W

            if "Publish " in action:
                action_name_rel_dict = {
                    "Publish Military Alliance": CountryRel.M,
                    "Publish Non-Intervention Treaty": CountryRel.T,
                    "Publish Peace Agreement": CountryRel.P,
                }
                for a, r in action_name_rel_dict.items():
                    if a == action:
                        # 更新公共关系库及己方国家关系库
                        self.country_relations[source_country][target_country] = r
                        self.country_relations[target_country][source_country] = r

                        # 更新己方国家关系库
                        self.country_relations_private[source_country][
                            target_country
                        ] = r
                        self.country_relations_private[target_country][
                            source_country
                        ] = r
                        break

            elif "Betray " in action:
                action_name_rel_dict = {
                    "Betray Military Alliance": CountryRel.N,
                    "Betray Non-Intervention Treaty": CountryRel.N,
                    "Betray Peace Agreement": CountryRel.N,
                }
                for a, r in action_name_rel_dict.items():
                    if a == action:
                        self.country_relations_private[source_country][
                            target_country
                        ] = r
                        self.country_relations_private[target_country][
                            source_country
                        ] = r

            elif "Accept " in action:
                action_name_rel_dict = {
                    "Accept Military Alliance": CountryRel.M,
                    "Accept Non-Intervention Treaty": CountryRel.T,
                    "Accept Peace Agreement": CountryRel.P,
                }
                for a, r in action_name_rel_dict.items():
                    if a == action:
                        self.country_relations_private[source_country][
                            target_country
                        ] = r
                        self.country_relations_private[target_country][
                            source_country
                        ] = r
                        break

            elif "Reject " in action:
                action_name_rel_dict = {
                    "Reject Military Alliance": CountryRel.N,
                    "Reject Non-Intervention Treaty": CountryRel.N,
                    "Reject Peace Agreement": CountryRel.N,
                }
                for a, r in action_name_rel_dict.items():
                    if a == action:
                        self.country_relations_private[source_country][
                            target_country
                        ] = r
                        self.country_relations_private[target_country][
                            source_country
                        ] = r
                        break

    def clone(self) -> "Board":
        import copy

        return copy.deepcopy(self)
