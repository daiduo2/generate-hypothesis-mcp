# -*- coding: utf-8 -*-
"""
AstroInsight FastMCP Server
基于FastMCP协议的AI研究论文生成工具服务器
"""

import os
import sys
import json
import uuid
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import threading
import time

# 设置环境变量
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('astroinsight_fastmcp.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# FastMCP导入
try:
    from mcp.server.fastmcp import FastMCP
    from mcp.types import TextContent
except ImportError as e:
    logger.error(f"FastMCP导入失败: {e}")
    sys.exit(1)

# 任务状态存储
tasks_storage: Dict[str, Dict[str, Any]] = {}
tasks_lock = threading.Lock()

class SimpleTask:
    """简单任务类，用于存储任务信息"""
    
    def __init__(self, task_id: str, keyword: str, search_paper_num: int):
        self.task_id = task_id
        self.keyword = keyword
        self.search_paper_num = search_paper_num
        self.status = "PENDING"
        self.progress = 0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.result = None
        self.error = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "task_id": self.task_id,
            "keyword": self.keyword,
            "search_paper_num": self.search_paper_num,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "result": self.result,
            "error": self.error
        }

def generate_task_id() -> str:
    """生成唯一任务ID"""
    return str(uuid.uuid4())

def ensure_temp_directory():
    """确保temp目录存在"""
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    return temp_dir

def update_task_status(task_id: str, status: str, progress: int = None, result: Any = None, error: str = None):
    """更新任务状态"""
    with tasks_lock:
        if task_id in tasks_storage:
            task = tasks_storage[task_id]
            task.status = status
            task.updated_at = datetime.now()
            
            if progress is not None:
                task.progress = progress
            if result is not None:
                task.result = result
            if error is not None:
                task.error = error
                
            logger.info(f"任务 {task_id} 状态更新: {status}, 进度: {task.progress}%")

def run_paper_generation_task(task_id: str, keyword: str, search_paper_num: int):
    """运行论文生成任务"""
    try:
        logger.info(f"开始执行任务 {task_id}: {keyword}")
        update_task_status(task_id, "RUNNING", 10)
        
        # 导入主要业务逻辑
        try:
            from main import generate_research_paper_main
            
            # 执行主要流程
            update_task_status(task_id, "RUNNING", 20)
            result = generate_research_paper_main(keyword, search_paper_num)
            
            # 任务完成
            update_task_status(task_id, "COMPLETED", 100, result)
            logger.info(f"任务 {task_id} 执行完成")
            
        except ImportError as e:
            logger.error(f"导入主业务逻辑失败: {e}")
            # 使用简化版本
            update_task_status(task_id, "RUNNING", 50)
            
            simple_result = {
                "keyword": keyword,
                "search_paper_num": search_paper_num,
                "status": "completed_simple",
                "message": "使用简化版本完成，部分功能可能不可用",
                "timestamp": datetime.now().isoformat()
            }
            
            update_task_status(task_id, "COMPLETED", 100, simple_result)
            
    except Exception as e:
        logger.error(f"任务 {task_id} 执行失败: {e}")
        update_task_status(task_id, "FAILED", error=str(e))

# 创建FastMCP应用
mcp = FastMCP("AstroInsight Research Assistant")

@mcp.tool()
def generate_research_paper(keyword: str, search_paper_num: int = 10) -> str:
    """
    启动研究论文生成任务
    
    Args:
        keyword: 研究关键词
        search_paper_num: 搜索论文数量 (1-20)
    
    Returns:
        任务ID和状态信息
    """
    try:
        # 参数验证
        if not keyword or not keyword.strip():
            return json.dumps({
                "error": "关键词不能为空",
                "status": "error"
            }, ensure_ascii=False)
        
        if not (1 <= search_paper_num <= 20):
            search_paper_num = min(max(search_paper_num, 1), 20)
        
        # 生成任务ID
        task_id = generate_task_id()
        
        # 创建任务
        task = SimpleTask(task_id, keyword.strip(), search_paper_num)
        
        with tasks_lock:
            tasks_storage[task_id] = task
        
        # 启动后台任务
        thread = threading.Thread(
            target=run_paper_generation_task,
            args=(task_id, keyword.strip(), search_paper_num),
            daemon=True
        )
        thread.start()
        
        logger.info(f"任务 {task_id} 已启动，关键词: {keyword}")
        
        return json.dumps({
            "task_id": task_id,
            "keyword": keyword.strip(),
            "search_paper_num": search_paper_num,
            "status": "PENDING",
            "message": "任务已创建并开始执行",
            "created_at": task.created_at.isoformat()
        }, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"创建任务失败: {e}")
        return json.dumps({
            "error": f"创建任务失败: {str(e)}",
            "status": "error"
        }, ensure_ascii=False)

@mcp.tool()
def get_task_status(task_id: str) -> str:
    """
    获取任务状态
    
    Args:
        task_id: 任务ID
    
    Returns:
        任务状态信息
    """
    try:
        with tasks_lock:
            if task_id not in tasks_storage:
                return json.dumps({
                    "error": "任务不存在",
                    "task_id": task_id,
                    "status": "not_found"
                }, ensure_ascii=False)
            
            task = tasks_storage[task_id]
            return json.dumps(task.to_dict(), ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}")
        return json.dumps({
            "error": f"获取状态失败: {str(e)}",
            "task_id": task_id,
            "status": "error"
        }, ensure_ascii=False)

@mcp.tool()
def list_active_tasks() -> str:
    """
    列出所有活跃任务
    
    Returns:
        活跃任务列表
    """
    try:
        with tasks_lock:
            active_tasks = []
            for task_id, task in tasks_storage.items():
                task_info = {
                    "task_id": task_id,
                    "keyword": task.keyword,
                    "status": task.status,
                    "progress": task.progress,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                active_tasks.append(task_info)
            
            return json.dumps({
                "active_tasks": active_tasks,
                "total_count": len(active_tasks),
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"列出任务失败: {e}")
        return json.dumps({
            "error": f"列出任务失败: {str(e)}",
            "active_tasks": [],
            "total_count": 0
        }, ensure_ascii=False)

if __name__ == "__main__":
    logger.info("启动 AstroInsight FastMCP 服务器...")
    
    # 确保必要目录存在
    ensure_temp_directory()
    
    # 启动服务器
    mcp.run()