import pydantic


class CountryProfile(pydantic.BaseModel):
    leader_ship: str
    """The leader ship of the country"""

    military_capability: str

    natural_industry_resource: str

    history_background: str

    key_policy: str

    public_morale: str
