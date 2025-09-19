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
    """运行论文生成任务的函数"""
    try:
        logger.info(f"开始执行论文生成任务: {task_id}")
        update_task_status(task_id, "STARTED", 10)
        
        # 导入main模块
        try:
            from main import main as run_main_process
            logger.info("成功导入main模块")
        except ImportError as e:
            error_msg = f"导入main模块失败: {e}"
            logger.error(error_msg)
            update_task_status(task_id, "FAILURE", error=error_msg)
            return
        
        update_task_status(task_id, "STARTED", 20)
        
        # 确保temp目录存在
        temp_dir = ensure_temp_directory()
        logger.info(f"临时目录已准备: {temp_dir}")
        
        update_task_status(task_id, "STARTED", 30)
        
        # 执行主要的论文生成流程
        logger.info(f"开始执行论文生成流程，关键词: {keyword}, 搜索论文数量: {search_paper_num}")
        
        # 调用main函数
        result = run_main_process(keyword, search_paper_num)
        
        update_task_status(task_id, "STARTED", 90)
        
        # 处理结果
        if result:
            logger.info(f"论文生成任务完成: {task_id}")
            update_task_status(task_id, "SUCCESS", 100, result)
        else:
            error_msg = "论文生成过程未返回有效结果"
            logger.error(error_msg)
            update_task_status(task_id, "FAILURE", error=error_msg)
            
    except Exception as e:
        error_msg = f"论文生成任务执行失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        update_task_status(task_id, "FAILURE", error=error_msg)

# 创建FastMCP应用
mcp = FastMCP("AstroInsight Research Assistant")

@mcp.tool()
def generate_research_paper(keyword: str, search_paper_num: int = 5) -> Dict[str, Any]:
    """
    生成研究论文的完整流程工具
    
    Args:
        keyword (str): 研究关键词，用于论文搜索和生成
        search_paper_num (int): 搜索论文数量，默认为5篇，范围1-20
        
    Returns:
        Dict[str, Any]: 包含任务ID和状态的字典
            - task_id: 任务唯一标识符
            - status: 任务状态 (PENDING, STARTED, SUCCESS, FAILURE)
            - message: 状态描述信息
            - keyword: 研究关键词
            - search_paper_num: 搜索论文数量
    """
    try:
        # 验证参数
        if not keyword or not keyword.strip():
            return {
                "error": "关键词不能为空",
                "status": "FAILURE"
            }
        
        if not isinstance(search_paper_num, int) or search_paper_num < 1 or search_paper_num > 20:
            return {
                "error": "搜索论文数量必须是1-20之间的整数",
                "status": "FAILURE"
            }
        
        # 生成任务ID
        task_id = generate_task_id()
        
        # 创建任务对象
        task = SimpleTask(task_id, keyword.strip(), search_paper_num)
        
        # 存储任务
        with tasks_lock:
            tasks_storage[task_id] = task
        
        # 在后台线程中启动任务
        thread = threading.Thread(
            target=run_paper_generation_task,
            args=(task_id, keyword.strip(), search_paper_num),
            daemon=True
        )
        thread.start()
        
        logger.info(f"论文生成任务已启动: {task_id}, 关键词: {keyword}, 论文数量: {search_paper_num}")
        
        return {
            "task_id": task_id,
            "status": "PENDING",
            "message": "论文生成任务已创建并开始执行",
            "keyword": keyword.strip(),
            "search_paper_num": search_paper_num
        }
        
    except Exception as e:
        error_msg = f"创建论文生成任务失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "error": error_msg,
            "status": "FAILURE"
        }

@mcp.tool()
def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    获取任务执行状态和结果
    
    Args:
        task_id (str): 任务ID，由generate_research_paper返回
        
    Returns:
        Dict[str, Any]: 任务状态信息
            - task_id: 任务ID
            - status: 任务状态
            - progress: 任务进度 (0-100)
            - created_at: 创建时间
            - updated_at: 更新时间
            - result: 任务结果 (成功时)
            - error: 错误信息 (失败时)
            - keyword: 研究关键词
    """
    try:
        if not task_id:
            return {
                "error": "任务ID不能为空",
                "status": "FAILURE"
            }
        
        with tasks_lock:
            if task_id not in tasks_storage:
                return {
                    "error": f"未找到任务ID: {task_id}",
                    "status": "NOT_FOUND"
                }
            
            task = tasks_storage[task_id]
            return task.to_dict()
            
    except Exception as e:
        error_msg = f"获取任务状态失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "error": error_msg,
            "status": "FAILURE"
        }

@mcp.tool()
def list_active_tasks() -> Dict[str, Any]:
    """
    列出所有当前活跃的任务及其状态
    
    Returns:
        Dict[str, Any]: 包含活跃任务列表的字典
            - tasks: 任务列表
            - total_count: 任务总数
            - timestamp: 查询时间戳
    """
    try:
        with tasks_lock:
            active_tasks = []
            for task_id, task in tasks_storage.items():
                # 只返回最近的任务或正在进行的任务
                if task.status in ["PENDING", "STARTED"] or \
                   (datetime.now() - task.updated_at).total_seconds() < 3600:  # 1小时内的任务
                    active_tasks.append(task.to_dict())
            
            # 按创建时间排序
            active_tasks.sort(key=lambda x: x["created_at"], reverse=True)
            
            return {
                "tasks": active_tasks,
                "total_count": len(active_tasks),
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        error_msg = f"获取活跃任务列表失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "error": error_msg,
            "status": "FAILURE",
            "tasks": [],
            "total_count": 0,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    try:
        logger.info("启动AstroInsight FastMCP服务器...")
        logger.info("服务器配置:")
        logger.info(f"- 工作目录: {os.getcwd()}")
        logger.info(f"- Python版本: {sys.version}")
        logger.info(f"- 编码设置: {sys.getdefaultencoding()}")
        
        # 确保temp目录存在
        ensure_temp_directory()
        
        # 运行服务器
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("服务器被用户中断")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}", exc_info=True)
        sys.exit(1)