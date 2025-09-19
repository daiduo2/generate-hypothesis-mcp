#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/9/21 23:07
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import arxiv
import json
import time
import logging
from typing import List, Dict, Any

# 配置日志
logger = logging.getLogger(__name__)

def get_authors(authors, first_author=False):
    """
    获取作者信息
    
    Args:
        authors: 作者列表
        first_author: 是否只返回第一作者
        
    Returns:
        str: 作者信息字符串
    """
    if not first_author:
        output = ", ".join(str(author) for author in authors)
    else:
        output = authors[0]
    return output


def get_papers(query="astronomy", max_results=2, timeout=30, max_retries=3):
    """
    从ArXiv获取论文信息
    
    Args:
        query: 搜索查询字符串
        max_results: 最大结果数量
        timeout: 超时时间（秒）
        max_retries: 最大重试次数
        
    Returns:
        List[Dict]: 论文信息列表
    """
    paper_list = []
    
    # 限制最大结果数量以避免过载
    if max_results > 100:
        logger.warning(f"限制搜索结果数量从 {max_results} 到 100 以避免过载")
        max_results = 100
    
    for attempt in range(max_retries):
        try:
            logger.info(f"开始搜索ArXiv论文，查询: {query}, 最大结果: {max_results} (尝试 {attempt + 1}/{max_retries})")
            
            # 创建搜索引擎，设置超时
            search_engine = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            # 设置超时时间
            start_time = time.time()
            result_count = 0
            
            # 使用新的迭代方法替代弃用的results()方法
            for result in search_engine.results():
                # 检查超时
                if time.time() - start_time > timeout:
                    logger.warning(f"ArXiv搜索超时 ({timeout}秒)，已获取 {result_count} 个结果")
                    break
                
                paper_id = result.entry_id
                paper_title = result.title
                paper_pdf = result.pdf_url
                paper_doi = result.doi
                paper_abstract = result.summary.replace("\n", " ")
                paper_authors = get_authors(result.authors)
                primary_category = result.primary_category
                publish_time = result.published.date().isoformat()

                data = {"topic": query,
                        "title": paper_title,
                        "id": paper_id,
                        "doi": paper_doi,
                        "pdf": paper_pdf,
                        "abstract": paper_abstract,
                        "authors": paper_authors,
                        "category": primary_category,
                        "time": publish_time}

                paper_list.append(data)
                result_count += 1
                
                # 添加小延迟以避免过快请求
                time.sleep(0.1)
            
            logger.info(f"成功获取 {len(paper_list)} 篇论文")
            break
            
        except Exception as e:
            logger.error(f"ArXiv搜索失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                logger.error("所有重试都失败了，返回空列表")
                return []
            time.sleep(2 ** attempt)  # 指数退避
    
    return paper_list


def search_paper(Keywords, Limit=2):
    """
    搜索论文的简化接口
    
    Args:
        Keywords: 搜索关键词
        Limit: 结果限制数量
        
    Returns:
        List[Dict]: 论文信息列表
    """
    data_collector = get_papers(query=Keywords, max_results=Limit)
    return data_collector