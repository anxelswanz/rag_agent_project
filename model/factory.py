from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.language_models import BaseChatModel
from project.utils.config_handler import rag_conf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatGoogleGenerativeAI(
            model=rag_conf["chat_model_name"],  # 或使用"deepseek-reasoner"（深度思考模型）
            google_api_key=rag_conf["api_key"] # DeepSeek API地址
        )

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        # return OllamaEmbeddings(
        #     model=rag_conf["embedding_model_name"],
        #     base_url="http://localhost:11434"
        # )
        return GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            api_key=rag_conf["api_key"]
        )

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()