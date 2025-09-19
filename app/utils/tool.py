#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/8/19 16:08
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import os
import re
import json
import logging
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)

def save_to_file(data: Any, file_path: str) -> bool:
    """
    保存数据到文件
    
    Args:
        data: 要保存的数据
        file_path: 文件路径
        
    Returns:
        bool: 保存是否成功
    """
    try:
        # 确保目录存在
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                f.write(str(data))
        
        logger.info(f"数据已保存到: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"保存文件失败: {e}")
        return False

def load_from_file(file_path: str) -> Any:
    """
    从文件加载数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        Any: 加载的数据
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.json'):
                return json.load(f)
            else:
                return f.read()
                
    except Exception as e:
        logger.error(f"加载文件失败: {e}")
        return None

def format_paper_info(paper: Dict[str, Any]) -> str:
    """
    格式化论文信息
    
    Args:
        paper: 论文信息字典
        
    Returns:
        str: 格式化后的论文信息
    """
    try:
        title = paper.get('title', '未知标题')
        authors = ', '.join(paper.get('authors', []))
        abstract = paper.get('abstract', '无摘要')
        published = paper.get('published', '未知日期')
        
        formatted = f"""
标题: {title}
作者: {authors}
发表日期: {published}
摘要: {abstract[:200]}...
        """.strip()
        
        return formatted
        
    except Exception as e:
        logger.error(f"格式化论文信息失败: {e}")
        return "论文信息格式化失败"

def remove_number_prefix(paragraph: str) -> str:
    """
    移除段落开头的数字前缀
    
    Args:
        paragraph: 输入段落
        
    Returns:
        str: 处理后的段落
    """
    # 使用正则表达式匹配开头的数字和点号
    pattern = r'^\d+\.\s*'
    return re.sub(pattern, '', paragraph)

def read_markdown_file(file_path: str) -> str:
    """
    读取Markdown文件内容
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"读取Markdown文件失败: {e}")
        return ""

def extract_hypothesis(file_content: str, split_section: str = "Hypothesis") -> List[str]:
    """
    从文件内容中提取假设
    
    Args:
        file_content: 文件内容
        split_section: 分割标记
        
    Returns:
        List[str]: 提取的假设列表
    """
    try:
        # 简单的文本分割和提取逻辑
        sections = file_content.split(split_section)
        hypotheses = []
        
        for section in sections[1:]:  # 跳过第一个部分
            # 提取假设内容
            lines = section.split('\n')
            hypothesis_lines = []
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    hypothesis_lines.append(line)
                    
            if hypothesis_lines:
                hypotheses.append('\n'.join(hypothesis_lines[:5]))  # 取前5行
                
        return hypotheses
        
    except Exception as e:
        logger.error(f"提取假设失败: {e}")
        return []

def search_releated_paper(topic: str, max_paper_num: int = 5, compression: bool = True, user_id: str = "", task=None) -> List[Dict[str, Any]]:
    """
    搜索相关论文
    
    Args:
        topic: 研究主题
        max_paper_num: 最大论文数量
        compression: 是否压缩
        user_id: 用户ID
        task: 任务对象
        
    Returns:
        List[Dict[str, Any]]: 相关论文列表
    """
    try:
        logger.info(f"搜索相关论文: {topic}")
        
        # 这里应该调用实际的论文搜索API
        # 暂时返回模拟数据
        papers = [
            {
                "title": f"关于{topic}的研究论文",
                "authors": ["研究者A", "研究者B"],
                "abstract": f"这是一篇关于{topic}的研究论文摘要",
                "published": "2024-01-01",
                "url": "https://example.com/paper"
            }
        ]
        
        return papers[:max_paper_num]
        
    except Exception as e:
        logger.error(f"搜索相关论文失败: {e}")
        return []

def extract_message(file_content: str, split_section: str) -> Dict[str, Any]:
    """
    从文件内容中提取消息
    
    Args:
        file_content: 文件内容
        split_section: 分割标记
        
    Returns:
        Dict[str, Any]: 提取的消息
    """
    try:
        sections = file_content.split(split_section)
        
        extracted_info = {
            "sections": len(sections),
            "content": sections[0] if sections else "",
            "extracted_at": "2024-01-01"
        }
        
        return extracted_info
        
    except Exception as e:
        logger.error(f"提取消息失败: {e}")
        return {"error": str(e)}

def extract_technical_entities(file_content: str, split_section: str) -> List[Dict[str, Any]]:
    """
    提取技术实体
    
    Args:
        file_content: 文件内容
        split_section: 分割标记
        
    Returns:
        List[Dict[str, Any]]: 技术实体列表
    """
    try:
        # 简单的技术实体提取逻辑
        entities = []
        
        # 查找常见的技术术语模式
        tech_patterns = [
            r'\b[A-Z]{2,}\b',  # 大写缩写
            r'\b\w+(?:AI|ML|DL|CNN|RNN|LSTM|GAN)\w*\b',  # AI相关术语
            r'\b\w*(?:algorithm|method|model|framework)\w*\b'  # 技术方法
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, file_content, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "entity": match,
                    "type": "technical",
                    "confidence": 0.8
                })
        
        # 去重
        unique_entities = []
        seen = set()
        for entity in entities:
            if entity["entity"].lower() not in seen:
                seen.add(entity["entity"].lower())
                unique_entities.append(entity)
        
        return unique_entities[:10]  # 返回前10个
        
    except Exception as e:
        logger.error(f"提取技术实体失败: {e}")
        return []