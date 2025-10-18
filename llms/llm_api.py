import openai
import yaml
from pprint import pprint
from loguru import logger

logger.remove()
logger.add("logs/llm_api.log", rotation="500 MB", encoding="utf-8")
# 读取config.yaml文件
# %%
with open("config.yaml", "r") as file:
    try:
        config = yaml.safe_load(file)
        logger.info(config)
    except yaml.YAMLError as exc:
        logger.error(exc)
# %%
# print(config.keys())
# print(config["ktransformers"]["base_url"])
client = openai.OpenAI(
    base_url=config["ktransformers"]["base_url"],
    api_key=config["ktransformers"]["api_key"],
)
# print(client.models.list())

res = client.chat.completions.create(
    model=config["ktransformers"]["model"],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是什么模型？"},
    ],
)
pprint(res)
pprint(res.choices[0].message.content)
