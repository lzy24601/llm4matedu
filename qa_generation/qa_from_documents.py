"""
1. 读文件
2. 解析文件
3. 文件分块
4. 生成问答
"""

from llms import local_llm
from utils.document_processor import DocumentProcessor

file_path = ""
document_processor = DocumentProcessor(file_path)
document_chunks = document_processor.split_document()
prompt = """
请根据以下内容一道单选题：
{}
"""
llm = local_llm()
