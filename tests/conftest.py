import os
import sys

# 将吸纳蘑菇根目录加入模块搜索路径，确保"from server.app.main import app"可用
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
