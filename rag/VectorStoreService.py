import os.path

from langchain_chroma import Chroma
from qdrant_client.http.models import Document

from project.utils.config_handler import chroma_conf
from project.model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from project.utils.path_tool import get_abs_path
from project.utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_nd5_hex
from project.utils.log_handler import logger

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf['collection_name'],
            embedding_function=embed_model,
            persist_directory=chroma_conf['persist_directory'],
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separator"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转入向量库
        要计算MD5去重
        :return:
        """

        def check_md5_hex(md5_for_check: str):
            abs_path = get_abs_path(chroma_conf["md5_hex_store"])
            if not os.path.exists(abs_path):
                open(abs_path, "w", encoding="utf-8").close()
                return False

            with open(abs_path, "r", encoding="utf-8") as file:
                # 正确读取所有行并存入集合，判断是否存在
                processed_md5s = {line.strip() for line in file if line.strip()}
                return md5_for_check in processed_md5s

        def save_md5_hex(md5_for_check: str):
            abs_path = get_abs_path(chroma_conf["md5_hex_store"])
            # 使用 "a" 模式追加，而不是 "w" 覆盖
            with open(abs_path, "a", encoding="utf-8") as file:
                file.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)
            return []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
             tuple(chroma_conf["allow_knowledge_file_type"])
        )

        for path in allowed_files_path:
            print(path)
            md5_hex = get_file_nd5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库] {path} 内容已存在")
                continue
            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"[加载知识库] {path}")
                    continue

                split_document: list[Document] = self.splitter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库] {path}")
                    continue

                self.vector_store.add_documents(split_document)

                # 记录已经处理好的md5
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库] {path} 内容加载成功..")
            except Exception as e:
                # exc_info为True会记录详细的报错
                logger.error(f"[加在知识库] {path} 加载失败..{str(e)}", exc_info=True)

if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("电池寿命一般多久？ 正常使用 2-3 年左右，容量会随充放电次数衰减。")
    for r in res:
        print(f"content: {r.page_content}")
        print("-"*20)
