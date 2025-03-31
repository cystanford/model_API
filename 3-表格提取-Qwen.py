import json
import os
import dashscope
from dashscope.api_entities.dashscope_response import Role
dashscope.api_key = "sk-"
from openai import OpenAI

# 封装模型响应函数
def get_response(messages):
    response = dashscope.MultiModalConversation.call(
        model='qwen-vl-plus',
        messages=messages
    )
    return response

content = [
    {'image': 'https://aiwucai.oss-cn-huhehaote.aliyuncs.com/pdf_table.jpg'}, # Either a local path or an url
    {'text': '这是一个表格图片，帮我提取里面的内容，输出JSON格式'}
]

messages=[{"role": "user", "content": content}]
# 得到响应
response = get_response(messages)
print(response)


# In[2]:


print(response.output.choices[0].message.content[0]['text'])

