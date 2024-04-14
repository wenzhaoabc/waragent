from typing import override

import pydantic


class CountryProfile(pydantic.BaseModel):
    leader_ship: str
    """The leader ship of the country"""

    military_capability: str

    natural_industry_resource: str

    history_background: str

    key_policy: str

    public_morale: str

    country_name: str

    profile_id: str

    def __str__(self):
        return f"CountryProfile: {self.country_name} - {self.leader_ship} - {self.military_capability}"


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

WWI_Profiles = [
    # profile of Country Britain
    CountryProfile(
        leader_ship="King George V",
        military_capability="High",
        natural_industry_resource="High",
        history_background="The British Empire was the largest empire in history and for a "
                           "considerable time was the foremost global power. By 1913, the British Empire held sway "
                           "over 412"
                           "million people, 23% of the world population at the time, and by 1920, it covered 35,500,"
                           "000 km2 (13,700,000 sq mi), 24% of the Earth's total land area. As a result, "
                           "its political, legal, linguistic, and cultural legacy is widespread. At the peak of its "
                           "power, it was described as the empire on which the sun never sets, as the sun was always "
                           "shining on at least one of its territories.",
    ),
    CountryProfile(
        leader_ship="King George V",
        military_capability="High", )
]
