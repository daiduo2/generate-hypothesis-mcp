#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/7/7 14:06
# @Author : 桐
# @QQ:1041264242
# 注意事项：

import json
import tiktoken
from dashscope import Generation
import dashscope
from openai import OpenAI
from app.core.config import DEEPSEEK_API_KEY, QWEN_API_KEY


def calculate_token_cost(text, model_name="gpt-3.5-turbo"):
    """
    计算给定文本的token成本
    
    Args:
        text (str): 要计算token的文本
        model_name (str): 模型名称，默认为gpt-3.5-turbo
    
    Returns:
        int: token数量
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        tokens = encoding.encode(text)
        return len(tokens)
    except Exception as e:
        print(f"Error calculating tokens: {e}")
        return 0


def call_with_deepseek(system_prompt, question):
    """
    使用DeepSeek模型进行对话
    
    Args:
        system_prompt (str): 系统提示词
        question (str): 用户问题
    
    Returns:
        str: 模型回复
    """
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    
    return response.choices[0].message.content


def call_with_deepseek_jsonout(system_prompt, question):
    """
    使用DeepSeek模型进行对话，返回JSON格式
    
    Args:
        system_prompt (str): 系统提示词
        question (str): 用户问题
    
    Returns:
        str: JSON格式的模型回复
    """
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        response_format={
            'type': 'json_object'
        },
        stream=False
    )
    
    return response.choices[0].message.content


def call_with_qwenmax(system_prompt, question):
    """
    使用QwenMax模型进行对话
    
    Args:
        system_prompt (str): 系统提示词
        question (str): 用户问题
    
    Returns:
        str: 模型回复
    """
    dashscope.api_key = QWEN_API_KEY
    
    response = Generation.call(
        model='qwen-max',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': question}
        ],
        result_format='message',
    )
    
    return response.output.choices[0]['message']['content']


def call_with_qwenmax_jsonout(system_prompt, question):
    """
    使用QwenMax模型进行对话，返回JSON格式
    
    Args:
        system_prompt (str): 系统提示词
        question (str): 用户问题
    
    Returns:
        str: JSON格式的模型回复
    """
    dashscope.api_key = QWEN_API_KEY
    
    response = Generation.call(
        model='qwen-max',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': question}
        ],
        result_format='message',
    )
    
    return response.output.choices[0]['message']['content']