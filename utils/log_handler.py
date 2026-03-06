import os
import logging
from datetime import datetime
# 假设 get_abs_path 已经正确导入
# from path_tool import get_abs_path

LOG_ROOT = "logs" # 示例路径
os.makedirs(LOG_ROOT, exist_ok=True)

# 1. 定义格式字符串
LOG_STR_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
# 2. 创建 Formatter 对象
formatter = logging.Formatter(LOG_STR_FORMAT)

def get_logger(name: str = "agent", log_file=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 防止重复添加 Handler
    if logger.handlers:
        return logger

    # 控制台 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter) # 使用定义好的 formatter
    logger.addHandler(console_handler)

    # 文件 Handler
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter) # 使用定义好的 formatter
    logger.addHandler(file_handler)

    # 关键点：禁用日志向上传递给 root logger，防止产生重复日志
    logger.propagate = False

    return logger

# 获取日志实例
logger = get_logger()

if __name__ == "__main__":
    logger.info("这是一条测试信息")
    logger.error("这是一条错误信息")