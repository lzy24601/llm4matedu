import pathlib
from utils.document_processor import DocumentProcessor
from qa_generation.qa_generator import QAGenerator

qa_generator = QAGenerator("/home/fstar/lzy/llm4matedu/config.yaml")
document_processor = DocumentProcessor()
now__dir__ = "/home/fstar/lzy/llm4matedu/data/markdowns"
path = []
for file in pathlib.Path(now__dir__).rglob("*"):
    if file.suffix.lower() == ".md":
        path.append(file)
# res = dp.read_document(document_type=".md", documents_path=path)
doc_content = document_processor.split_documents(
    document_type=".md", documents_path=path
)

qa = []
cnt = 0
for doc_name, chunks in doc_content.items():
    for chunk in chunks:
        if cnt >= 1:
            break
        qa.append(qa_generator.generate_qa_from_documents(chunk))
        cnt += 1

print(qa)
