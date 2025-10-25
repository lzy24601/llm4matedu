import os
import pathlib
import pdfplumber
from chonkie import TokenChunker
from typing import List, Union


class DocumentProcessor:
    def __init__(self, document_path, document_type=None):
        """
        初始化文档处理器

        Args:
            document_path (str): 文档或文件夹路径
            document_type (list, optional): 要处理的文件类型列表，默认为[".pdf", ".doc", ".docx"]

        Raises:
            FileNotFoundError: 当指定的路径不存在时
        """
        # 设置默认的文件类型列表，避免使用可变对象作为默认参数
        if document_type is None:
            document_type = [".pdf", ".doc", ".docx"]

        try:
            # 将传入的路径字符串转换为pathlib.Path对象
            path = pathlib.Path(document_path)

            # 检查路径是否存在
            if not os.path.exists(document_path):
                raise FileNotFoundError(f"路径{document_path} 不存在")

            # 递归查找所有匹配文件类型的文件
            self.documents_path = [
                file
                for file in path.rglob("*")
                if file.is_file() and file.suffix.lower() in document_type
            ]

            # 初始化TokenChunker对象
            self.chunker = TokenChunker(chunk_size=512, chunk_overlap=128)
        except Exception as e:
            print(f"初始化文档处理器时出错: {str(e)}")
            # 可以选择重新抛出异常或设置默认值
            self.documents_path = []
            # self.chunker = None  # 或者根据实际需求决定是否初始化chunker

    def split_document(self):
        document_record = self.read_document(self.documents_path)
        document_chunks = {}
        for document_name, document_content in document_record.items():
            document_chunks[document_name] = self.chunker(document_content)
        return document_chunks

    def read_document(
        self,
        documents_path: Union[str, pathlib.Path, List[Union[str, pathlib.Path]]] = None,
    ):
        # 如果没有指定文档路径，使用初始化时的文档路径
        if documents_path is None:
            documents_path = self.documents_path
        if isinstance(documents_path, (str, pathlib.Path)):
            documents_path = [documents_path]
        document_record = {}
        for document_path in documents_path:
            path = pathlib.Path(document_path)
            if path.suffix.lower() == ".pdf":
                document_record[path.name] = self.read_pdf(path)
            elif path.suffix.lower() in [".doc", ".docx"]:
                document_record[path.name] = self.read_doc(path)
            else:
                print(f"不支持的文件类型 {path.suffix}")
                return None
        return document_record

    def read_pdf(self, pdf_file_path: Union[str, pathlib.Path]):
        """
        读取PDF文件并提取其中的文本内容

        Args:
            pdf_file_path (str or pathlib.Path): PDF文件的路径，可以是字符串或Path对象

        Returns:
            str: 从PDF文件中提取的所有文本内容，出错时返回空字符串
        """
        try:
            # 将传入的文件路径转换为pathlib.Path对象
            pdf_file_path = pathlib.Path(pdf_file_path)

            # 使用pdfplumber库打开PDF文件
            with pdfplumber.open(pdf_file_path) as pdf:
                print(f"读取文件 {pdf_file_path}")
                text = ""

                # 遍历PDF文件中的每一页
                for page in pdf.pages:
                    # 安全地提取文本，处理可能的None值
                    page_text = page.extract_text() or ""
                    text += page_text

            return text
        except Exception as e:
            print(f"读取PDF文件 {pdf_file_path} 时出错: {str(e)}")
            return ""

    def read_doc(self, doc_file_path: Union[str, pathlib.Path]):
        pass

    def save_content(self):
        pass


if __name__ == "__main__":
    dp = DocumentProcessor("/home/fstar/lzy/llm4matedu/data/pdfs")
    path = dp.documents_path[0]
    res = dp.split_document()
    for document_name, document_chunks in res.items():
        print(document_name)
        for chunk in document_chunks:
            print(chunk)
            break
        print(document_chunks)
        exit()
