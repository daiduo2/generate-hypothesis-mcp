#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/11/2 19:08
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import warnings
import agentscope
from agentscope import msghub
from agentscope.agents import DialogAgent, UserAgent
from agentscope.message import Msg
from app.core.config import OUTPUT_PATH
import os
from app.core.tpl import tpl_env

# 抑制SQLAlchemy相关警告
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sqlalchemy")
warnings.filterwarnings("ignore", message=".*SQLAlchemy.*")

model_configs = [
    {
        "config_name": "qwen-max-2025-01-25",
        "model_type": "dashscope_chat",
        "model_name": "qwen-max",
        "api_key": "sk-586f6f96d2704df6901e31de27fda2fe",
    },
    {
        "config_name": "qwen-plus",
        "model_type": "dashscope_chat",
        "model_name": "qwen-plus",
        "api_key": "sk-586f6f96d2704df6901e31de27fda2fe",
    },
    {
        "config_name": "glm-4-long",
        "model_type": "openai_chat",
        "model_name": "glm-4-long",
        "api_key": "1cf7ad6057486482907576343cdfad25.Pj3NWFDgjyjNqDVK",
        "client_args": {
            "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        },
    },
    {
        "config_name": "deepseek-chat",
        "model_type": "openai_chat",
        "model_name": "deepseek-chat",
        "api_key": "sk-80cc66e836004e6ca698eb35206dd418",
        "client_args": {
            "base_url": "https://api.deepseek.com/v1",
        },
    },
    {
        "config_name": "moonshot-v1-8k",
        "model_type": "openai_chat",
        "model_name": "moonshot-v1-8k",
        "api_key": "sk-u66x82yZ6tMcjRMOwkKouZDHrhrLmLGl3ghjOlxOBUuvw6MD",
        "client_args": {
            "base_url": "https://api.moonshot.cn/v1",
        },
    },
    {
        "config_name": "gemini-2.5-flash",
        "model_type": "gemini_chat",
        "model_name": "gemini-2.5-flash",
        "api_key": "AIzaSyCRuZMYqpQZAt7wlSsqXGjXcwxUekrrH4s",
    },
    {
        "config_name": "hunyuan-large",
        "model_type": "openai_chat",
        "model_name": "hunyuan-large",
        "api_key": "sk-O5wisGpuwAS6FM7ICWtOM049vWYyEGq3opa4wSf920zeimW4",
        "client_args": {
            "base_url": "https://api.hunyuan.cloud.tencent.com/v1",
        },
    }
]


def moa_idea_iteration(topic="", user_prompt="", user_id="", task=None):
    """
    MOA思想迭代函数
    
    Args:
        topic: 研究主题
        user_prompt: 用户提示
        user_id: 用户ID
        task: 任务对象
    
    Returns:
        str: 聚合后的内容
    """
    # MOA实现逻辑
    pass


def moa_model(model_configs, agent_list, topic, user_prompt, systeam_prompt, ac_prompt="", ac_systeam="", stage=""):
    """
    MOA模型函数
    
    Args:
        model_configs: 模型配置列表
        agent_list: 代理列表
        topic: 主题
        user_prompt: 用户提示
        systeam_prompt: 系统提示
        ac_prompt: 聚合提示
        ac_systeam: 聚合系统提示
        stage: 阶段
    
    Returns:
        str: 处理结果
    """
    # MOA模型实现逻辑
    pass


def moa_table(model_configs=model_configs, topic='', draft='', user_id='', task=None):
    """
    MOA表格函数
    
    Args:
        model_configs: 模型配置
        topic: 主题
        draft: 草稿
        user_id: 用户ID
        task: 任务对象
    
    Returns:
        str: 表格结果
    """
    # MOA表格实现逻辑
    pass