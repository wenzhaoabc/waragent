import unittest

from src.llm import LLM, Text2Image


class TestLLM(unittest.TestCase):
    def test_llm(self):
        llm = LLM("yi-34b-chat-0205")
        res = llm.chat("Hi, Please tell me your name. The format of your output should be : My name is <NAME>.")
        self.assertGreater(len(res), 0, msg=f"llm response if {res}")

    def test_vl_model(self):
        llm = LLM("gpt-4-turbo-1")
        with self.assertRaises(ValueError):
            res = llm.chat_v("Please describe the picture in general. Thanks!",
                             img_url="https://picsum.photos/id/201/200", callback=lambda x: print(x), )

    def test_vl_model_2(self):
        llm = LLM("gpt-4-turbo")
        res = llm.chat_v("Please describe the picture in general. Thanks!",
                         img_url="https://picsum.photos/id/201/400", callback=lambda x: print(x))
        self.assertGreater(len(res), 0, msg=f"llm response if {res}")

    def test_generate_image(self):
        t2i = Text2Image("cogview-3")
        res = t2i.generate_image("a red apple on a white plate", "a blue apple on a black plate")
        self.assertGreater(len(res), 0, msg=f"llm response if {res}")


if __name__ == '__main__':
    unittest.main()
