from src.history.agent_actions import Action
from src.history.profile import CountryProfile
from src.llm import LLM
from .board import Board
from .stick import Stick
from .secretary import SecretaryAgent


class CountryAgent(object):
    def __init__(self,
                 identity: str,
                 profile: CountryProfile,
                 actions: list[Action],
                 secretary: SecretaryAgent,
                 llm: LLM,
                 board: Board,
                 stick: Stick
                 ) -> None:
        pass

    def generate_action(self, prompt: str) -> list[Action]:
        pass
