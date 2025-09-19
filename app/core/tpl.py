from jinja2 import Environment, FileSystemLoader
import os

# 使用绝对路径确保模板加载不受工作目录影响
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
templates_dir = os.path.join(project_root, "app", "templates")

file_loader = FileSystemLoader(templates_dir)
tpl_env = Environment(loader=file_loader, enable_async=True)