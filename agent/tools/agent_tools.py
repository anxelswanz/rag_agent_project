import os.path
import random
import datetime

from langchain_core.tools import tool
from project.rag.rag_service import RagSummarizeService
from project.utils.config_handler import agent_conf
from project.utils.path_tool import get_abs_path
from project.utils.log_handler import logger
rag = RagSummarizeService()
external_data = {}

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="获取制定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    return f"城市{city}天气为晴天，空气湿度50%"

@tool(description="获取用户所在城市的名称，以纯字符串的形式返回")
def get_user_city() -> str:
    return random.choice(["深圳", "长沙"])

@tool(description="获取用户的id")
def get_user_id() -> str:
    return "001"

@tool(description="获取当月月份")
def get_current_month() -> str:
    return str(datetime.date.today().month)

def generate_external_data():
    """

    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")
                user_id: str = arr[0].replace('"',"")
                print("user_id:", user_id)
                feature: str = arr[1].strip().replace('"',"")
                efficiency: str = arr[2].strip().replace('"',"")
                consumables: str = arr[3].strip().replace('"', "")
                contrast: str = arr[4].strip().replace('"', "")
                print("contrast:", contrast)
                time: str = arr[5].strip().replace('"',"")
                print("time:", time)
                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "feature": feature,
                    "efficiency": efficiency,
                    "consumables": consumables,
                    "time": time,
                }
        print(external_data)
@tool(description="获取外部系统中获取用户使用记录，以纯字符串形式返回，如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()
    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户{user_id}在{month}的使用记录数据")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景注入上下文信息")
def fill_context_for_report():
    return "fill_context_for_report调用"

if __name__ == '__main__':
    print(fetch_external_data("1001", "2026.12.23"))

