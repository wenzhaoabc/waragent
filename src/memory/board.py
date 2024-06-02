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
                for target in [c for c in self.country_names if country != c]
            }
            for country in self.country_names
        }

        # dict[str, dict[str, list[Action]]]
        # 每一轮次，每个国家对其他国家的动作
        self.country_actions = {
            country: {
                target: [] for target in [c for c in self.country_names if country != c]
            }
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
        index = 0
        for acs in self.history:
            history_text += (
                f"In No {index + 1} day:" + "\n".join([ac.message for ac in acs]) + "\n"
            )
            index += 1

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

    def set_country_rel(
        self,
        country_source: str,
        country_target: str,
        rel: CountryRel,
        public: bool = True,
    ) -> None:
        self.country_relations_private[country_target][country_source] = rel
        self.country_relations_private[country_source][country_target] = rel
        if public:
            self.country_relations[country_target][country_source] = rel
            self.country_relations[country_source][country_target] = rel

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

            if not target_country:
                continue

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
                self.country_relations_private[source_country][
                    target_country
                ] = CountryRel.W
                self.country_relations_private[target_country][
                    source_country
                ] = CountryRel.W

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
                        self.country_relations[source_country][target_country] = r
                        self.country_relations[target_country][source_country] = r
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
                        pass

    def get_countries_rel(
        self, source_country: str, round_time: int
    ) -> tuple[dict, dict]:
        """
        获取国际政治情形，获取处于结盟/不干预/和平协定的国家
        :param source_country: 以该国家为视角总结国际关系
        :param round_time: 当前模拟进行的轮次

        :return: source_country的国家关系，其它国家的国家关系
        """
        # if round_time == 1:
        #     return {}, {}

        other_countries_rels = {}
        for source, rels in self.country_relations.items():
            if source == source_country:
                continue
            for t, r in rels.items():
                if t == source_country:
                    continue
                if r != CountryRel.N:
                    c1 = sorted([source, t])[0]
                    c2 = sorted([source, t])[1]
                    other_countries_rels.update({c1: {c2: r}})

        self_countries_rels = {}

        for t, r in self.country_relations_private[source_country].items():
            if r != CountryRel.N:
                if r in self_countries_rels.keys():
                    self_countries_rels[r].append(t)
                else:
                    self_countries_rels[r] = [t]

        return self_countries_rels, other_countries_rels

    def summary_countries_rel(self, source_country: str, round_time: int) -> str:
        """总结国际政治关系"""
        self_countries_rels, other_countries_rels = self.get_countries_rel(
            source_country, round_time
        )
        current_situation = ""
        for r, countries in self_countries_rels.items():
            if r == CountryRel.M:
                current_situation += (
                    f"forged a military alliance with {' '.join(countries)}, "
                )
            elif r == CountryRel.T:
                current_situation += f"forged a non-intervention treatment alliance with {' '.join(countries)}, "
            elif r == CountryRel.P:
                current_situation += (
                    f"forged a peace agreement alliance with {' '.join(countries)}, "
                )
            elif r == CountryRel.W:
                current_situation += f"and are at war with {' '.join(countries)}. "

        nl_str = {
            CountryRel.W: "at war",
            CountryRel.M: "forged military alliance",
            CountryRel.T: "forged non-intervention treaties",
            CountryRel.P: "forged peace agreement",
        }

        current_situation_other = ""
        for c, rels in other_countries_rels.items():
            # assert isinstance(c, str)
            # assert isinstance(rels, dict)
            current_situation_other += f"\n{c} has {', '.join([nl_str.get(v) + ' with ' + k for k, v in rels.items()])}."
        if current_situation_other:
            current_situation += "\nFor other countries:" + current_situation_other
            
        if current_situation:
            return "You have " + current_situation
        return current_situation

    def output_rels(self) -> str:
        res = ""
        res += f"  {' '.join([n.split(' ')[1] for n in self.country_names])}\n"
        i = 0
        for c, rels in self.country_relations.items():
            temp_arr = [r for t, r in rels.items()]
            temp_arr.insert(i, "/")
            res += f"{c.split(' ')[1]} {'  '.join(temp_arr)}\n"
            i += 1

        return res

    def output_rels_pri(self) -> str:
        res = ""
        res += f"  {' '.join([n.split(' ')[1] for n in self.country_names])}\n"
        i = 0
        for c, rels in self.country_relations_private.items():
            temp_arr = [r for t, r in rels.items()]
            temp_arr.insert(i, "/")
            res += f"{c.split(' ')[1]} {'  '.join(temp_arr)}\n"
            i += 1

        return res

    def clone(self) -> "Board":
        import copy

        return copy.deepcopy(self)


# from src.profiles import CountryProfileList

# b = Board(CountryProfileList)

# b.set_country_rel("Country GE", "Country PO", CountryRel.W)

# p = b.get_countries_rel("Country GE", 1)

# print(p)
