from base_llm import BaseLLM

import openai
import yaml
from pprint import pprint
from loguru import logger
from pathlib import Path


class LocalLLM(BaseLLM):

    def __init__(self, config_file="config.yaml"):
        with open(config_file, "r") as file:
            try:
                config = yaml.safe_load(file)
                logger.info(config)
                self.model = config["ktransformers"]["model"]
                self.base_url = config["ktransformers"]["base_url"]
                self.api_key = config["ktransformers"]["api_key"]
            except yaml.YAMLError as exc:
                logger.error(exc)
        self.client = openai.OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def make_request(
        self,
        prompts,
        max_tokens=10240,
        temperature=0.5,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=None,
        logprobs=None,
        n=1,
        best_of=1,
        retries=3,
    ):
        response = None
        retry_cnt = 0
        while retry_cnt < retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=prompts,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=stop,
                    logprobs=logprobs,
                    n=n,
                )
                print(response)
                print(type(response))
                break
            except openai.OpenAIError as e:
                logger.error(f"OpenAI API error: {e}")
                retry_cnt += 1
        if response is not None:
            return response.choices[0].message.content


if __name__ == "__main__":
    llm = LocalLLM()
    messages = [
        {"role": "system", "content": "你是一个出题专家"},
        {"role": "user", "content": "帮我出一道python单选题，并在最后一行输出答案"},
    ]
    res = llm.make_request(messages)
    pprint(res)
