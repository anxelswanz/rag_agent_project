import os, hashlib

from onnxruntime.transformers.shape_infer_helper import file_path
from log_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_nd5_hex(filePath: str): # 获取md5的16进制字符串
    if not os.path.exists(file_path):
        logger.error(f"File {file_path} does not exist")
        return
    if not os.path.isfile(filePath):
        logger.error(f"File {file_path} is not a file")
        return
    md5_obj = hashlib.md5()
    chunk_size = 4096 #4kb分片，避免文件过大爆内存
    try:
        with open(filePath, "rb") as f:  # 必须二进制
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"file {filePath} md5 failed")

def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):  # 返回文件夹内的文件列表
    files = []
    if not os.path.isdir(path):
        logger.error(f"path {path} is not a directory")
        return allowed_types

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(f)

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)

def pdf_loader(filepath: str, password=None):
    return PyPDFLoader(filepath, password=password).load()

def txt_loader() -> list[Document]:
    return TextLoader().load()



