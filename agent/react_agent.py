from langchain.agents import create_agent
from project.model.factory import chat_model
from project.utils.prompt_loader import load_system_prompt

from project.agent.tools.agent_tools import (rag_summarize, get_weather, get_user_id, get_user_city,
                                             get_current_month, fetch_external_data, fill_context_for_report)
from project.agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_weather, get_user_id, get_user_city, get_current_month, fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )
    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        # 第三个参数context就是上下文runtime中的信息，就是我们做提示词切换的标记
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                #在 Agent 中的作用： 由于 AI 生成内容可能需要很久（比如 10 秒），如果用 return，用户必须等 10 秒才能看到结果。
                # 使用 yield，Agent 每想好一句话或一个片段，就立刻“吐”给前端，实现打字机效果。
                yield latest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在我所在的地区如何保养"):
        print(chunk, end="", flush=True)