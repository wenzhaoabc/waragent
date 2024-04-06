import unittest

from src.llm import LLM


class TestLLM(unittest.TestCase):
    def test_llm(self):
        llm = LLM("yi-34b-chat-0205")
        res = llm.chat("Hi, Please tell me your name.")
        self.assertGreater(len(res), 0, msg=f"llm response if {res}")


if __name__ == '__main__':
    unittest.main()
