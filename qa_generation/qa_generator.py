from llms.local_llm import LocalLLM


class QAGenerator:
    def __init__(self, config_file=None) -> None:
        self.llm = LocalLLM(config_file)

    def generate_qa_from_documents(self, document_content, qa_nums=3):
        messages = [
            {"role": "system", "content": "你是一个出题专家"},
            {
                "role": "user",
                "content": f"""你是一个概率论专家，请根据下面内容提出一道有四个选项的单选题\n
                {document_content}
            """,
            },
        ]
        qa = self.llm.make_request(messages)

        return qa

    def generate_question_from_seeds(self):
        pass

    def generate_answer_from_question(self):
        pass
