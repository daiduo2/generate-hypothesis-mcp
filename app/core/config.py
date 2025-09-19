#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/9/21 23:07
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    应用配置类
    """
    # 应用基础配置
    APP_NAME: str = "AstroInsight"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # API配置
    API_V1_STR: str = "/api/v1"
    
    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # LLM API配置
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    
    # ArXiv API配置
    ARXIV_MAX_RESULTS: int = 10
    ARXIV_TIMEOUT: int = 30
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def get_config():
    """获取配置实例"""
    return Settings()

settings = Settings()