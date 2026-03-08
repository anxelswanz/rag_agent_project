
"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料交给模型，让模型回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from project.rag.VectorStoreService import VectorStoreService
from project.utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from project.model.factory import chat_model


def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagSummarizeService:
    def __init__(self):
        self.victor_store = VectorStoreService()
        self.retriever = self.victor_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self.__init__chain()

    def __init__chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:

        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"[参考资料 {counter}]: 参考资料 {doc.page_content} | 参考元数据: {doc.metadata} \n"

        return self.chain.invoke(
            {
                "input": query,
                "context": context
            }
        )

if __name__ == '__main__':
    rag = RagSummarizeService()
    rag.rag_summarize("小户型适合哪种扫地机器人")