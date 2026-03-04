from pkg_resources import file_ns_handler

from path_tool import get_abs_path
import os, logging
from datetime import datetime


LOG_ROOT = get_abs_path("logs")

os.makedirs(LOG_ROOT, exist_ok=True)
DEFAULT_LOF_FORMAT = logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
)

def get_logger(name: str = "agent",
               log_file = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(DEFAULT_LOF_FORMAT)

    logger.addHandler(console_handler)

    # 文件handler
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(DEFAULT_LOF_FORMAT)

    logger.addHandler(file_handler)

    return logger


# 快捷获取日志
logger = get_logger()

if __name__ == "__main__":
    logger.info("信息")
    logger.error("错误")