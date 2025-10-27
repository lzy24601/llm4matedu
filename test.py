import pathlib
import pymupdf4llm

pdf = pathlib.Path("/home/fstar/lzy/llm4matedu/data/pdfs/ch3.2.pdf")
print(pdf.suffix)
# md = pymupdf4llm.to_markdown(pdf)

# print(type(md))
# pathlib.Path("output.md").write_bytes(md.encode())
