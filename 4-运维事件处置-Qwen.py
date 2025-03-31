"""
1、告警内容理解。根据输入的告警信息，结合第三方接口数据，判断当前的异常情况（告警对象、异常模式）；
2、分析方法建议。根据当前告警内容，结合应急预案、运维文档和大语言模型自有知识，形成分析方法的建议；
3、分析内容自动提取。根据用户输入的分析内容需求，调用多种第三方接口获取分析数据，并进行总结；
4、处置方法推荐和执行。根据当前上下文的故障场景理解，结合应急预案和第三方接口，形成推荐处置方案，待用户确认后调用第三方接口进行执行。
"""
import json
import os
import random
import dashscope
from dashscope.api_entities.dashscope_response import Role
dashscope.api_key = "sk-"
from openai import OpenAI

# 通过第三方接口获取数据库服务器状态
def get_current_status():
    # 生成连接数数据
    connections = random.randint(10, 100)
    # 生成CPU使用率数据
    cpu_usage = round(random.uniform(1, 100), 1)
    # 生成内存使用率数据
    memory_usage = round(random.uniform(10, 100), 1)
    status_info = {
        "连接数": connections,
        "CPU使用率": f"{cpu_usage}%",
        "内存使用率": f"{memory_usage}%"
    }
    return json.dumps(status_info, ensure_ascii=False)

# 封装模型响应函数
def get_response(messages):
    response = dashscope.Generation.call(
        model='qwen-turbo',
        messages=messages,
        tools=tools,
        result_format='message'  # 将输出设置为message形式
    )
    return response
    
current_locals = locals()
current_locals

tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_status",
                "description": "调用监控系统接口，获取当前数据库服务器性能指标，包括：连接数、CPU使用率、内存使用率",
                "parameters": {
                },
                "required": []
            }                
        }
    ]

query = """告警：数据库连接数超过设定阈值
时间：2024-08-03 15:30:00
"""
messages=[
    {"role": "system", "content": "我是运维分析师，用户会告诉我们告警内容。我会基于告警内容，判断当前的异常情况（告警对象、异常模式）"},
    {"role": "user", "content": query}]


# In[2]:


while True:
    response = get_response(messages)
    message = response.output.choices[0].message
    messages.append(message)
    #print('response=', response)

    if response.output.choices[0].finish_reason == 'stop':
        break
    
    # 判断用户是否要call function
    if message.tool_calls:
        # 获取fn_name, fn_arguments
        fn_name = message.tool_calls[0]['function']['name']
        fn_arguments = message.tool_calls[0]['function']['arguments']
        arguments_json = json.loads(fn_arguments)
        #print(f'fn_name={fn_name} fn_arguments={fn_arguments}')
        function = current_locals[fn_name]
        tool_response = function(**arguments_json)
        tool_info = {"name": "get_current_weather", "role":"tool", "content": tool_response}
        #print('tool_info=', tool_info)
        messages.append(tool_info)

print(messages)

