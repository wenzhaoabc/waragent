import datetime
import unittest

from src.utils import upload_file_to_oss, download_file_from_oss, migrate_img_oss


class OSSTest(unittest.TestCase):
    def test_oss(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f"test/{timestamp}.txt"
        content = b"test content"
        url = upload_file_to_oss(file_path, content)
        self.assertGreater(len(url), 0, msg=f"upload to oss failed: url:{url}")
        self.assertEqual(content, download_file_from_oss(file_path))

    def test_migration(self):
        url = "https://api.postman.com/collections/32072597-dd2111b5-b84f-4b71-9646-8a93d71adae0?access_key=PMAT-01HVB8G3JMW7H79J3VPQNW1Q09"
        prompt = "test"
        res = migrate_img_oss(url, prompt)
        self.assertGreater(len(res), 0, msg=f"migrate to oss failed: url:{url} prompt:{prompt} res:{res}")


if __name__ == '__main__':
    unittest.main()
