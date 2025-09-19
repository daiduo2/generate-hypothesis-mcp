# -*- coding: utf-8 -*-
"""
AstroInsight 主要业务逻辑
研究论文生成的核心流程实现
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# 设置环境变量
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 导入必要的模块
try:
    from app.utils.arxiv_api import search_papers, download_paper_info
    from app.utils.llm_api import call_llm_api
    from app.core.config import get_config
    from app.core.prompt import get_prompt_template
    from app.core.moa import run_moa_optimization
    from app.utils.tool import save_to_file, load_from_file, format_paper_info
except ImportError as e:
    logging.warning(f"部分模块导入失败: {e}")
    # 如果导入失败，使用简化版本
    pass

# 配置日志
logger = logging.getLogger(__name__)

def process_paper(paper_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理单篇论文信息
    
    Args:
        paper_info: 论文信息字典
        
    Returns:
        处理后的论文信息
    """
    try:
        processed_info = {
            "title": paper_info.get("title", ""),
            "authors": paper_info.get("authors", []),
            "abstract": paper_info.get("abstract", ""),
            "published": paper_info.get("published", ""),
            "url": paper_info.get("url", ""),
            "summary": paper_info.get("summary", ""),
            "categories": paper_info.get("categories", []),
            "doi": paper_info.get("doi", "")
        }
        
        # 格式化作者信息
        if isinstance(processed_info["authors"], list):
            processed_info["authors_str"] = ", ".join(processed_info["authors"])
        else:
            processed_info["authors_str"] = str(processed_info["authors"])
            
        # 格式化发布日期
        if processed_info["published"]:
            try:
                # 尝试解析日期格式
                if isinstance(processed_info["published"], str):
                    processed_info["published_formatted"] = processed_info["published"][:10]
                else:
                    processed_info["published_formatted"] = str(processed_info["published"])[:10]
            except Exception:
                processed_info["published_formatted"] = processed_info["published"]
        
        return processed_info
        
    except Exception as e:
        logger.error(f"处理论文信息时出错: {e}")
        return paper_info

def extract_facts_from_papers(papers: List[Dict[str, Any]], keyword: str) -> Dict[str, Any]:
    """
    从论文中提取事实信息
    
    Args:
        papers: 论文列表
        keyword: 搜索关键词
        
    Returns:
        提取的事实信息
    """
    try:
        logger.info(f"开始从 {len(papers)} 篇论文中提取事实信息")
        
        # 构建论文摘要文本
        papers_text = ""
        for i, paper in enumerate(papers, 1):
            processed_paper = process_paper(paper)
            papers_text += f"\n\n=== 论文 {i} ===\n"
            papers_text += f"标题: {processed_paper['title']}\n"
            papers_text += f"作者: {processed_paper.get('authors_str', '')}\n"
            papers_text += f"发布日期: {processed_paper.get('published_formatted', '')}\n"
            papers_text += f"摘要: {processed_paper['abstract']}\n"
            
        # 获取事实提取提示模板
        try:
            from app.core.tpl import get_template
            fact_extraction_prompt = get_template('fact_extraction_prompt.tpl')
            prompt = fact_extraction_prompt.render(
                keyword=keyword,
                papers_text=papers_text
            )
        except Exception as e:
            logger.warning(f"模板加载失败，使用默认提示: {e}")
            prompt = f"""
            请从以下论文中提取与关键词 "{keyword}" 相关的核心事实信息：
            
            {papers_text}
            
            请提取：
            1. 核心概念和定义
            2. 主要研究方法
            3. 重要发现和结论
            4. 技术细节和参数
            5. 数据集和实验设置
            
            请以结构化的方式组织这些信息。
            """
        
        # 调用LLM提取事实
        try:
            from app.utils.llm_api import call_with_deepseek
            facts_response = call_with_deepseek(prompt)
            
            facts_info = {
                "keyword": keyword,
                "papers_count": len(papers),
                "extracted_facts": facts_response,
                "extraction_time": datetime.now().isoformat(),
                "papers_summary": papers_text[:1000] + "..." if len(papers_text) > 1000 else papers_text
            }
            
            logger.info("事实信息提取完成")
            return facts_info
            
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            # 返回基础信息
            return {
                "keyword": keyword,
                "papers_count": len(papers),
                "extracted_facts": "事实提取失败，请检查LLM配置",
                "extraction_time": datetime.now().isoformat(),
                "error": str(e)
            }
            
    except Exception as e:
        logger.error(f"事实提取过程出错: {e}")
        return {
            "keyword": keyword,
            "papers_count": len(papers) if papers else 0,
            "extracted_facts": f"提取失败: {str(e)}",
            "extraction_time": datetime.now().isoformat(),
            "error": str(e)
        }

def generate_hypothesis(facts_info: Dict[str, Any], keyword: str) -> Dict[str, Any]:
    """
    基于事实信息生成研究假设
    
    Args:
        facts_info: 提取的事实信息
        keyword: 研究关键词
        
    Returns:
        生成的假设信息
    """
    try:
        logger.info("开始生成研究假设")
        
        # 获取假设生成提示模板
        try:
            from app.core.tpl import get_template
            hypothesis_prompt = get_template('hypothesis_generate_prompt.tpl')
            prompt = hypothesis_prompt.render(
                keyword=keyword,
                facts=facts_info.get('extracted_facts', ''),
                papers_count=facts_info.get('papers_count', 0)
            )
        except Exception as e:
            logger.warning(f"模板加载失败，使用默认提示: {e}")
            prompt = f"""
            基于以下事实信息，为关键词 "{keyword}" 生成创新的研究假设：
            
            事实信息：
            {facts_info.get('extracted_facts', '')}
            
            请生成：
            1. 3-5个具有创新性的研究假设
            2. 每个假设的理论依据
            3. 可能的验证方法
            4. 预期的研究贡献
            
            请确保假设具有科学性、可验证性和创新性。
            """
        
        # 调用LLM生成假设
        try:
            from app.utils.llm_api import call_with_deepseek
            hypothesis_response = call_with_deepseek(prompt)
            
            hypothesis_info = {
                "keyword": keyword,
                "generated_hypothesis": hypothesis_response,
                "based_on_facts": facts_info.get('extracted_facts', '')[:500] + "...",
                "generation_time": datetime.now().isoformat(),
                "papers_count": facts_info.get('papers_count', 0)
            }
            
            logger.info("研究假设生成完成")
            return hypothesis_info
            
        except Exception as e:
            logger.error(f"假设生成LLM调用失败: {e}")
            return {
                "keyword": keyword,
                "generated_hypothesis": "假设生成失败，请检查LLM配置",
                "generation_time": datetime.now().isoformat(),
                "error": str(e)
            }
            
    except Exception as e:
        logger.error(f"假设生成过程出错: {e}")
        return {
            "keyword": keyword,
            "generated_hypothesis": f"生成失败: {str(e)}",
            "generation_time": datetime.now().isoformat(),
            "error": str(e)
        }

def optimize_research_idea(hypothesis_info: Dict[str, Any], keyword: str) -> Dict[str, Any]:
    """
    优化研究想法
    
    Args:
        hypothesis_info: 假设信息
        keyword: 研究关键词
        
    Returns:
        优化后的研究想法
    """
    try:
        logger.info("开始优化研究想法")
        
        # 尝试使用MOA优化
        try:
            from app.core.moa import moa_idea_iteration
            optimized_result = moa_idea_iteration(
                keyword=keyword,
                hypothesis=hypothesis_info.get('generated_hypothesis', ''),
                papers_info=hypothesis_info.get('based_on_facts', '')
            )
            
            optimization_info = {
                "keyword": keyword,
                "original_hypothesis": hypothesis_info.get('generated_hypothesis', ''),
                "optimized_idea": optimized_result,
                "optimization_method": "MOA (Mixture of Agents)",
                "optimization_time": datetime.now().isoformat()
            }
            
            logger.info("研究想法优化完成")
            return optimization_info
            
        except Exception as e:
            logger.warning(f"MOA优化失败，使用简单优化: {e}")
            
            # 简单优化方案
            try:
                from app.utils.llm_api import call_with_deepseek
                
                optimization_prompt = f"""
                请对以下研究假设进行技术优化和完善：
                
                关键词: {keyword}
                原始假设: {hypothesis_info.get('generated_hypothesis', '')}
                
                请从以下角度进行优化：
                1. 技术可行性分析
                2. 创新点突出
                3. 实验设计建议
                4. 预期成果和影响
                5. 潜在挑战和解决方案
                
                请提供一个完整、优化的研究方案。
                """
                
                optimized_response = call_with_deepseek(optimization_prompt)
                
                optimization_info = {
                    "keyword": keyword,
                    "original_hypothesis": hypothesis_info.get('generated_hypothesis', ''),
                    "optimized_idea": optimized_response,
                    "optimization_method": "Simple LLM Optimization",
                    "optimization_time": datetime.now().isoformat()
                }
                
                return optimization_info
                
            except Exception as e:
                logger.error(f"简单优化也失败: {e}")
                return {
                    "keyword": keyword,
                    "original_hypothesis": hypothesis_info.get('generated_hypothesis', ''),
                    "optimized_idea": "优化失败，请检查配置",
                    "optimization_method": "Failed",
                    "optimization_time": datetime.now().isoformat(),
                    "error": str(e)
                }
                
    except Exception as e:
        logger.error(f"研究想法优化过程出错: {e}")
        return {
            "keyword": keyword,
            "original_hypothesis": hypothesis_info.get('generated_hypothesis', ''),
            "optimized_idea": f"优化失败: {str(e)}",
            "optimization_method": "Error",
            "optimization_time": datetime.now().isoformat(),
            "error": str(e)
        }

def generate_research_paper_main(keyword: str, search_paper_num: int = 10) -> Dict[str, Any]:
    """
    主要的研究论文生成流程
    
    Args:
        keyword: 研究关键词
        search_paper_num: 搜索论文数量
        
    Returns:
        完整的研究结果
    """
    try:
        logger.info(f"开始生成研究论文，关键词: {keyword}, 论文数量: {search_paper_num}")
        
        result = {
            "keyword": keyword,
            "search_paper_num": search_paper_num,
            "start_time": datetime.now().isoformat(),
            "status": "processing"
        }
        
        # 步骤1: 搜索论文
        logger.info("步骤1: 搜索相关论文")
        try:
            from app.utils.arxiv_api import get_papers
            papers = get_papers(keyword, max_results=search_paper_num)
            result["papers"] = papers
            result["papers_found"] = len(papers)
            logger.info(f"找到 {len(papers)} 篇相关论文")
        except Exception as e:
            logger.error(f"论文搜索失败: {e}")
            result["papers"] = []
            result["papers_found"] = 0
            result["search_error"] = str(e)
        
        # 步骤2: 提取事实信息
        logger.info("步骤2: 提取事实信息")
        facts_info = extract_facts_from_papers(result.get("papers", []), keyword)
        result["facts_info"] = facts_info
        
        # 步骤3: 生成假设
        logger.info("步骤3: 生成研究假设")
        hypothesis_info = generate_hypothesis(facts_info, keyword)
        result["hypothesis_info"] = hypothesis_info
        
        # 步骤4: 优化研究想法
        logger.info("步骤4: 优化研究想法")
        optimization_info = optimize_research_idea(hypothesis_info, keyword)
        result["optimization_info"] = optimization_info
        
        # 完成
        result["status"] = "completed"
        result["end_time"] = datetime.now().isoformat()
        result["total_duration"] = "处理完成"
        
        logger.info("研究论文生成流程完成")
        return result
        
    except Exception as e:
        logger.error(f"研究论文生成主流程出错: {e}")
        return {
            "keyword": keyword,
            "search_paper_num": search_paper_num,
            "status": "error",
            "error": str(e),
            "end_time": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # 测试代码
    test_keyword = "machine learning"
    test_result = generate_research_paper_main(test_keyword, 5)
    print(json.dumps(test_result, indent=2, ensure_ascii=False))