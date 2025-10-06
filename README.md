
# K12-Agent 

## 环境与快速开始
- 要求：Python 3.11+、git
- 创建虚拟环境并安装依赖:
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```

- 启动后端与验证
```bash
uvicorn server.app.main:app --host 127.0.0.2 --port 8000
```
```bash
curl http://127.0.0.1:8000/health
```

- 运行测试:
```bash
pytest -q
```

## 目录结构（当前阶段）
- `server/app/main.py`：后端入口（GET /health）
- `tests/test_health.py`：第一个单元测试
- `requirements.txt`：后端依赖
- `.gitignore`：忽略虚拟环境与缓存

