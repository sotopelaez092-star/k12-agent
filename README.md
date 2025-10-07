
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

# 框架文档（完整版）

## 项目简介
- 目标：搭建“前后端通信与调度框架”的可复用基线，确保契约一致、错误统一、日志可追踪
- 技术栈：FastAPI、Uvicorn、Pydantic、pytest、httpx、pytest-asyncio
- 关键特性：
  - 请求 ID 中间件：`X-Request-ID` 生成/透传，成功路径回传
  - 统一错误处理器：404/405/422/500 的统一 JSON 错误结构，错误路径回传 `X-Request-ID`
  - 结构化 JSON 日志：包含 `method`、`path`、`rid`、`status`、`duration_ms`
  - CORS：暴露 `X-Request-ID` 头，前端可读取用于链路追踪
  - 测试基线：健康/信息/就绪、错误、校验与请求 ID 传播

## 快速开始
- 环境要求：Python 3.11+、git
- 初始化与安装依赖：
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```
- 开发启动：
```bash
make dev
```
- 健康检查：
```bash
make health
```
- 运行测试：
```bash
make test
```

## 目录结构
- `server/app/main.py`：应用入口，组装路由与中间件
- `server/app/api/health.py`：系统路由（`/health`、`/ready`、`/info`、`/validate`）
- `server/app/handlers/middleware.py`：请求 ID 中间件、CORS 注册
- `server/app/handlers/errors.py`：统一错误处理器（404/405/422/500）
- `server/app/logging.py`：结构化 JSON 日志 formatter
- `server/app/settings.py`：应用与 CORS 配置（支持 `.env`）
- `tests/`：测试用例（健康、信息、就绪、错误、校验）

## 配置（Settings）
- 文件：`server/app/settings.py`
- 环境变量支持：`APP_` 前缀，例如：
  - `APP_LOG_LEVEL` 控制日志级别（默认 `INFO`）
  - `APP_HOST`、`APP_PORT` 设置启动端口（Makefile 中默认 `PORT=8001`）
- CORS 默认开发配置：
  - `cors_allow_origins=["*"]`
  - `cors_expose_headers=["X-Request-ID"]`
  - 生产建议改为白名单域名并从环境变量读取

## 中间件与错误处理
- 中间件（`RequestIDMiddleware`）职责：
  - 读取或生成 `X-Request-ID`（UUID），写入 `request.state.request_id`
  - 记录结构化请求日志（开始/结束，包含 `rid`、耗时、状态码等）
  - 成功响应路径在响应头写入 `X-Request-ID`
- 错误处理器职责：
  - 接管并统一错误响应结构
  - 在 404/405/422/500 响应头写入 `X-Request-ID`，保证错误路径可追踪

## 请求 ID 契约
- 客户端可传入 `X-Request-ID`，服务端透传并在响应头回传
- 未传入时服务端自动生成 UUID 并回传
- 成功路径由中间件写头；错误路径由错误处理器写头
- 前端读取响应头需要 CORS 的 `expose_headers=['X-Request-ID']`

## API 契约
- 成功响应：按路由定义返回业务 JSON
- 统一错误结构：
```json
{"error":{"code":<int>,"message":"<str>","details":[...]?}}
```
- 422 校验错误：
  - `message`: `"Validation Error"`
  - `details`: 来自 Pydantic 的 `exc.errors()`（含 `loc`、`msg`、`type`）

## 路由与示例
- `GET /health`：健康检查，返回 `{"status":"ok"}`
- `GET /ready`：就绪检查，返回 `{"ready":true}`
- `GET /info`：应用信息（`app_name`、`version`、`env`、`startup_time`）
- `POST /validate`：校验示例（请求体模型：`{"name":str,"age":int}`）
  - 校验成功：返回 `{"ok":true}`
  - 校验失败：返回 422 错误结构（含 `details`）

## CORS 配置与前端协作
- 已注册 `CORSMiddleware`，默认允许跨域并暴露 `X-Request-ID` 头
- 前端示例（fetch）：
```js
const resp = await fetch("http://127.0.0.1:8001/health", { method: "GET" });
const rid = resp.headers.get("X-Request-ID");
console.log(rid); // 用于链路追踪
```
- 生产将 `allow_origins` 改为白名单，例如：`["https://your-frontend.com"]`

## 日志规范（JSON）
- 每行日志为一个 JSON 对象：
  - 基础字段：`timestamp`、`level`、`logger`、`message`
  - 上下文字段（通过 `extra` 注入）：`method`、`path`、`rid`、`status`、`duration_ms`
- 示例：
```plaintext
{"timestamp":"2025-10-07T14:32:10","level":"INFO","logger":"request","message":"request_end","method":"GET","path":"/ready","rid":"...","status":200,"duration_ms":2.15}
```

## 测试与验证（逐步）
- 运行全部测试：
```bash
make test
```
- 验证成功路径的请求 ID：
```bash
curl -i http://127.0.0.1:8001/ready
# 响应头应包含 X-Request-ID；重复请求传入 RID 并检查回传：
curl -i http://127.0.0.1:8001/ready -H "X-Request-ID: test-rid-123"
```
- 验证 404/405 错误结构与请求 ID：
```bash
curl -i http://127.0.0.1:8001/not-exists
curl -i -X POST http://127.0.0.1:8001/health
# 期待 JSON 错误结构与响应头 X-Request-ID
```
- 验证 422 校验错误与请求 ID：
```bash
curl -i -X POST http://127.0.0.1:8001/validate \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","age":"bad"}'
# 返回 422，JSON 中含 details；响应头含 X-Request-ID
```
- 验证 CORS 预检（浏览器跨域场景）：
```bash
curl -i -X OPTIONS "http://127.0.0.1:8001/health" \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
```

## 提交与推送
- 提交：使用约定式消息（Makefile 已提供）
```bash
make commit MSG="docs(readme): 完整文档与验证步骤"
```
- 推送：
```bash
make push
```

## 复用指南
- 复制 `server/app` 与 `tests` 到新项目
- 调整 `settings.py`（`app_name`、`version`、`env`、CORS）
- 扩展业务路由到 `server/app/api/` 下，直接复用中间件与错误处理器
- 前端按约定读写 `X-Request-ID`，保证端到端追踪

## 常见问题
- 看不到 `X-Request-ID`：
  - 确认中间件已注册，错误处理器已生效
  - 浏览器需配置 `expose_headers=["X-Request-ID"]`（已配置）
- CORS 失败：
  - 开发默认 `allow_origins=["*"]`；生产改白名单
- 测试失败：
  - 先运行 `make test` 查看具体失败用例与断言
  - 确认端口与 HOST 一致（Makefile 默认 `HOST=127.0.0.1 PORT=8001`）