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

    input: InteractionContent
    """The input of the action"""

    output: InteractionContent
    """The output of the action"""


actions = [
    Action(
        name="list_countries",
        description="List all countries",
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
