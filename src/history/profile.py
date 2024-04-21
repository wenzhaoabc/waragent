import pydantic


class CountryProfile(pydantic.BaseModel):
    real_name: str
    """The real name of the country in history"""

    country_name: str
    """The name of the country"""

    leader_ship: str
    """The leader ship of the country"""

    military_capability: str
    """Military capability comprises quantitative data such as the size of its standing army, naval tonnage, and a qualitative assessment of its overall military strength, including any particular dominance in specific branches, such as naval or aerial forces."""

    natural_industry_resource: str
    """Information about the country's geographical topography, climatic conditions, products, etc"""

    history_background: str
    """Historical background incorporates the legacy of prior conflicts of interest and unresolved issues between nations, which can considerably influence current policies."""

    key_policy: str
    """Key policy outlines the principal objectives pursued by nations."""

    public_morale: str
    """Public morale reflects the populace’s sentiment, which can directly or indirectly influence a country’s action."""

    def __str__(self):
        return f"""
Country name: {self.country_name}
Leader ship: {self.leader_ship}
Military capability: {self.military_capability}
Natural industry resource: {self.natural_industry_resource}
History background: {self.history_background}
Key policy: {self.key_policy}
Public morale: {self.public_morale}
"""


"""
第二次世界大战，各国家的profile
第二次世界大战的主要参战国主要分为两个阵营：同盟国和轴心国。
同盟国主要包括：
英国：United Kingdom
美国：United States
中国：China
苏联：Soviet Union
法国：France
加拿大：Canada
澳大利亚：Australia
新西兰：New Zealand
印度：India
南非：South Africa

轴心国主要包括：
德国：Germany
日本：Japan
意大利：Italy
匈牙利：Hungary
罗马尼亚：Romania
保加利亚：Bulgaria
芬兰：Finland
"""
