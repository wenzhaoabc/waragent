import os

import oss2
import requests

from . import log


def upload_file_to_oss(file_path: str, content: str | bytes) -> str:
    auth = oss2.Auth(
        os.getenv("OSS_ACCESS_KEY_ID"),
        os.getenv("OSS_ACCESS_KEY_SECRET"),
    )
    bucket = oss2.Bucket(
        auth,
        os.getenv("OSS_ENDPOINT"),
        os.getenv("OSS_BUCKET_NAME"),
    )
    result = bucket.put_object(file_path, content)
    log.info(
        f"upload file to oss: file_path:{file_path} request_id:{result.request_id}"
    )
    if result.status == 200:
        return f"https://{os.getenv('OSS_BUCKET_NAME')}.{os.getenv('OSS_ENDPOINT')}/{file_path}"
    else:
        log.error(
            f"upload file to oss failed: file_path:{file_path} status:{result.status}"
        )
        return ""


def download_file_from_oss(file_path: str) -> bytes:
    auth = oss2.Auth(
        os.getenv("OSS_ACCESS_KEY_ID"),
        os.getenv("OSS_ACCESS_KEY_SECRET"),
    )
    bucket = oss2.Bucket(
        auth,
        os.getenv("OSS_ENDPOINT"),
        os.getenv("OSS_BUCKET_NAME"),
    )
    result_stream = bucket.get_object(file_path)
    result_bytes = result_stream.read()
    log.info(
        f"download file from oss: file_path:{file_path} request_id:{result_stream.request_id}"
    )
    if result_stream.client_crc != result_stream.server_crc:
        log.error(f"download file from oss failed: file_path:{file_path} crc not match")
        return bytes(0)
    if result_stream.status == 200:
        return result_bytes
    else:
        log.error(
            f"download file from oss failed: file_path:{file_path} status:{result_stream.status}"
        )
        return bytes(0)


def migrate_img_oss(file_url: str, prompt: str) -> str:
    url = os.getenv("FC_MIGRATE_OSS")
    res = requests.get(url, params={"url": file_url, "prompt": prompt})
    if res.status_code == 200:
        log.info(
            f"migrate to oss: url:{file_url} prompt:{prompt} status:{res.status_code} res:{res.json()}"
        )
        return res.json()["url"]
    else:
        log.error(
            f"migrate to oss failed: url:{file_url} prompt:{prompt} status:{res.status_code}"
        )
        return ""
