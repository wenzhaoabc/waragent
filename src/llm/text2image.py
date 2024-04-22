import os
import jwt
import time
import requests

from src.utils import log
from src.utils import migrate_img_oss


class Text2Image:
    models = ["stable-diffusion-xl", "dall-e-2", "dall-e-3", "cogview-3"]

    def __init__(self, model: str):
        self.model = model

    @staticmethod
    def generate_token(apikey: str, exp_seconds: int):
        try:
            key_id, secret = apikey.split(".")
        except Exception as e:
            raise Exception("invalid apikey", e)

        payload = {
            "api_key": key_id,
            "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
            "timestamp": int(round(time.time() * 1000)),
        }

        return jwt.encode(
            payload,
            secret,
            algorithm="HS256",
            headers={"alg": "HS256", "sign_type": "SIGN"},
        )

    def generate_by_cogview(self, prompt: str) -> list[str]:
        if self.model != "cogview-3":
            raise ValueError(f"model {self.model} doesn't support")
        jwt_token = self.generate_token(os.getenv("ZHIPU_API_KEY"), 10000)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt_token}"
        }
        request_json = {
            "prompt": prompt,
            "model": self.model
        }

        res = requests.post("https://open.bigmodel.cn/api/paas/v4/images/generations",
                            json=request_json, headers=headers)
        res_json = res.json()
        log.info(f"generate image by cogview3: prompt:{prompt} res:{res_json}")
        image_url = [item["url"] for item in res_json["data"]]
        return image_url

    def generate_by_sdxl(self, prompt: str, negative_prompt: str, callback: callable = None, size: str = "1024*1024",
                         n: int = 1, steps: int = 40, scale: int = 10, seed: int | None = None) -> list[str]:
        if self.model != "stable-diffusion-xl":
            raise ValueError(f"model {self.model} doesn't support")
        text2image_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
        res_get_url = "https://dashscope.aliyuncs.com/api/v1/tasks/"
        request_json = {
            "model": "stable-diffusion-xl",
            "input": {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
            },
            "parameters": {
                "size": size,
                "n": n,
                "steps": steps,
                "scale": scale,
            }
        }
        if seed is not None:
            request_json["parameters"]["seed"] = seed

        headers = {
            "X-DashScope-Async": "enable",
            "Authorization": f"Bearer {os.getenv("DASHSCOPE_API_KEY")}",
            "Content-Type": "application/json",
        }
        res = requests.post(text2image_url, json=request_json, headers=headers)
        res_json = res.json()

        log.info(
            f"generate image: prompt:{prompt} negative_prompt:{negative_prompt} res:{res_json}")

        task_id = res_json["output"]["task_id"]
        task_status = "PENDING"
        while task_status != "SUCCEEDED":
            #  get task result
            task_res = requests.get(res_get_url + task_id,
                                    headers={"Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"})
            task_res_json = task_res.json()
            task_status = task_res_json["output"]["task_status"]
            if task_status == "SUCCEEDED":
                image_url_list = [result["url"] for result in task_res_json["output"]["results"]]
                log.info(
                    f"generate image success: prompt:{prompt} negative_prompt:{negative_prompt} \
                     task_id:{task_id} image_url_list:{image_url_list}")
                if callback is not None:
                    callback(image_url_list)
                return image_url_list
            elif task_status == "FAILED" or task_status == "UNKNOWN":
                log.error(
                    f"generate image failed: prompt:{prompt} negative_prompt:{negative_prompt} res:{task_res_json}")
                return []

    def generate_image(self, prompt: str, negative_prompt: str, callback: callable = None, size: str = "1024*1024",
                       n: int = 1, steps: int = 40, scale: int = 10, seed: int | None = None) -> list[str]:
        image_url = []
        if self.model == "cogview-3":
            image_url = self.generate_by_cogview(prompt)
        elif self.model == "stable-diffusion-xl":
            image_url = self.generate_by_sdxl(prompt, negative_prompt, callback, size, n, steps, scale, seed)
        else:
            raise ValueError(f"model {self.model} doesn't support")

        oss_urls = []
        for url in image_url:
            oss_urls.append(migrate_img_oss(url, f"{prompt};{negative_prompt};{self.model}"))

        log.info(
            f"text to image: prompt:{prompt} negative_prompt:{negative_prompt} model:{self.model} oss_urls:{oss_urls}")
        return oss_urls

    def check_image_size(self, model: str) -> bool:
        model_size = {
            "stable-diffusion-xl": ["1024*1024"],
            "dall-e-2": ["256*256"],
            "dall-e-3": ["256*256"],
            "cogview-3": ["256*256"],
        }
        return self.model in model_size
