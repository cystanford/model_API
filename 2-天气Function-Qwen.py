import json
import os
import dashscope
from dashscope.api_entities.dashscope_response import Role
dashscope.api_key = "sk-"
from openai import OpenAI

# 编写你的函数
def get_current_weather(location, unit="摄氏度"):
    # 获取指定地点的天气
    temperature = -1
    if '大连' in location or 'Dalian' in location:
        temperature = 10
    if location=='上海':
        temperature = 36
    if location=='深圳':
        temperature = 37
    weather_info = {
        "location": location,
        "temperature": temperature,
        "unit": unit,
        "forecast": ["晴天", "微风"],
    }
    return json.dumps(weather_info)

# 封装模型响应函数
def get_response(messages):
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            messages=messages,
            functions=functions,
            result_format='message'
        )
        return response
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        return None

# 使用function call进行QA
def run_conversation():
    query = "大连的天气怎样"
    messages=[{"role": "user", "content": query}]
    
    # 得到第一次响应
    response = get_response(messages)
    if not response or not response.output:
        print("获取响应失败")
        return None
        
    print('response=', response)
    
    message = response.output.choices[0].message
    messages.append(message)
    print('message=', message)
    
    # Step 2, 判断用户是否要call function
    if hasattr(message, 'function_call') and message.function_call:
        function_call = message.function_call
        tool_name = function_call['name']
        # Step 3, 执行function call
        arguments = json.loads(function_call['arguments'])
        print('arguments=', arguments)
        tool_response = get_current_weather(
            location=arguments.get('location'),
            unit=arguments.get('unit'),
        )
        tool_info = {"role": "function", "name": tool_name, "content": tool_response}
        print('tool_info=', tool_info)
        messages.append(tool_info)
        print('messages=', messages)
        
        #Step 4, 得到第二次响应
        response = get_response(messages)
        if not response or not response.output:
            print("获取第二次响应失败")
            return None
            
        print('response=', response)
        message = response.output.choices[0].message
        return message
    return message

functions = [
    {
      'name': 'get_current_weather',
      'description': 'Get the current weather in a given location.',
      'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': 'The city and state, e.g. San Francisco, CA'
                },
                'unit': {'type': 'string', 'enum': ['celsius', 'fahrenheit']}
            },
        'required': ['location']
      }
    }
]

if __name__ == "__main__":
    result = run_conversation()
    if result:
        print("最终结果:", result)
    else:
        print("对话执行失败")

