import os
import pathlib
import pdfplumber
from chonkie import TokenChunker
from typing import List, Union
from .pdf2md import parse_doc


class DocumentProcessor:
    def __init__(self, document_path=None, document_type=None):
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
        self.pdf_file_path = []
        self.doc_file_path = []
        self.documents_path = []
        if document_path is not None:
            try:
                # 将传入的路径字符串转换为pathlib.Path对象
                path = pathlib.Path(document_path)

                # 检查路径是否存在
                if not os.path.exists(document_path):
                    raise FileNotFoundError(f"路径{document_path} 不存在")
                for file in path.rglob("*"):
                    if file.is_file():
                        if file.suffix.lower() == ".pdf":
                            self.pdf_file_path.append(file)

                        elif file.suffix.lower() == ".doc" or ".docx":
                            self.doc_file_path.append(file)

            except Exception as e:
                print(f"初始化文档处理器时出错: {str(e)}")
                # 可以选择重新抛出异常或设置默认值

    def split_documents(
        self,
        document_type: Union[str, List[str]] = None,
        documents_path: Union[str, pathlib.Path, List[Union[str, pathlib.Path]]] = None,
        split_method="token_level",
    ):
        if split_method == "token_level":
            # 初始化TokenChunker对象
            self.chunker = TokenChunker(chunk_size=512, chunk_overlap=0)
        document_record = self.read_document(
            document_type=document_type, documents_path=documents_path
        )
        document_chunks = {}
        for document_name, document_content in document_record.items():
            document_chunks[document_name] = self.chunker(document_content)
        return document_chunks

    def read_document(
        self,
        document_type: Union[str, List[str]] = None,
        documents_path: Union[str, pathlib.Path, List[Union[str, pathlib.Path]]] = None,
    ):
        # 如果没有指定文档路径，使用初始化时的文档路径
        if documents_path is None:
            documents_path = self.documents_path
        if isinstance(documents_path, (str, pathlib.Path)):
            documents_path = [documents_path]

        if document_type is None:
            document_type = [".md", ".pdf", ".doc", ".docx"]
        if isinstance(document_type, str):
            document_type = [document_type]

        document_record = {}
        for document_path in documents_path:
            path = pathlib.Path(document_path)
            if path.suffix.lower() not in document_type:
                continue
            if path.suffix.lower() == ".pdf":
                document_record[path.name] = self.read_pdf(path)
            elif path.suffix.lower() in [".doc", ".docx"]:
                document_record[path.name] = self.read_doc(path)
            elif path.suffix.lower() == ".md":
                document_record[path.name] = self.read_markdown(path)
            else:
                print(f"不支持的文件类型 {path.suffix}")
                return None
        return document_record

    def read_markdown(self, markdown_file_path: Union[str, pathlib.Path]):
        markdown_file_path = pathlib.Path(markdown_file_path)
        try:
            with open(markdown_file_path, "r", encoding="utf-8") as file:
                content = file.read()
                return content
        except Exception as e:
            print(f"读取文件失败{markdown_file_path}:{e}")
            return None

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

    def pdf2md(self, pdf_files_dir, output_dir, backend="pipeline"):
        pdf_suffixes = [".pdf"]

        # image_suffixes = ["png", "jpeg", "jp2", "webp", "gif", "bmp", "jpg"]

        doc_path_list = []
        for doc_path in pathlib.Path(pdf_files_dir).rglob("*"):
            if doc_path.suffix.lower() in pdf_suffixes:
                doc_path_list.append(doc_path)

        """如果您由于网络问题无法下载模型，可以设置环境变量MINERU_MODEL_SOURCE为modelscope使用免代理仓库下载模型"""
        # os.environ['MINERU_MODEL_SOURCE'] = "modelscope"

        """Use pipeline mode if your environment does not support VLM"""
        parse_doc(doc_path_list, output_dir, backend=backend)


if __name__ == "__main__":
    # dp = DocumentProcessor("/home/fstar/lzy/llm4matedu/data/pdfs")
    dp = DocumentProcessor()
    now__dir__ = "/home/fstar/lzy/llm4matedu/data/markdowns"
    path = []
    for file in pathlib.Path(now__dir__).rglob("*"):
        if file.suffix.lower() == ".md":
            path.append(file)
    # res = dp.read_document(document_type=".md", documents_path=path)
    res = dp.split_documents(document_type=".md", documents_path=path)
    print(res)
    # print(dp.pdf_file_path)
    # dp.pdf2md(
    #     "/home/fstar/lzy/llm4matedu/data/pdfs",
    #     "/home/fstar/lzy/llm4matedu/data/markdowns",
    # )
