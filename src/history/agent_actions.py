from typing import Literal

import pydantic


class InteractionContent(pydantic.BaseModel):
    type: str
    """The type of interaction content. Example list_countries, list_tuple_countries"""

    require: bool
    """The content of this interaction is required whether or not."""

    example: str
    """Example of the content of this interaction."""


class Action(pydantic.BaseModel):
    name: str
    """The name of the action. Identity filed"""

    description: str
    """The detail description of the action"""

    public: bool
    """Whether the action is public or not"""

    initiative: bool
    """The action is initiative or not"""

    require_response: bool
    """The action requires response or not"""

    input_type: Literal["list", "tuple"]
    """The input type of the action. Example: list for [Country A, Country B]"""


actions = [
    Action(
        name="Wait without Action",
        description="Wait without Action",
        public=True,
        input=InteractionContent(
            type="list_countries",
            example="list_countries",
            require=True,
        ),
        output=InteractionContent(
            type="list_countries",
            example="list_countries",
            require=False,
        ),
    )
]
