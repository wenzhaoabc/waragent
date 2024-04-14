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
        self.identity = identity
        self.profile = profile
        self.actions = actions
        self.secretary = secretary
        self.llm = llm
        self.board = board
        self.stick = stick

    def generate_action(self, prompt: str) -> list[Action]:
        """
        LLM output
        Action: <action_name>
        Target: <target_country> split by ','
        Input: <Action Input>

        :param prompt:
        :return:
        """
        pass
