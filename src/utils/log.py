import datetime
import logging
import os

# 创建一个logger
logger = logging.getLogger('system')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_path = os.getenv("ROOT_PATH")
fh = logging.FileHandler(f'{log_path}/{filename}.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)-7s : %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
