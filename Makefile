HOST ?= 127.0.0.1
PORT ?= 8001
LOG_LEVEL ?= INFO
UVICORN ?= uvicorn

.PHONY: dev stop ready health info test commit push

dev:
	APP_LOG_LEVEL=$(LOG_LEVEL) $(UVICORN) server.app.main:app --host $(HOST) --port $(PORT) --reload

stop:
	@PID=$$(lsof -ti tcp:$(PORT)); \
	if [ -n "$$PID" ]; then \
		echo "Stopping process on port $(PORT): $$PID"; \
		kill $$PID; \
	else \
		echo "No process found on port $(PORT)"; \
	fi

ready:
	curl -s http://$(HOST):$(PORT)/ready

health:
	curl -s http://$(HOST):$(PORT)/health

info:
	curl -s http://$(HOST):$(PORT)/info

test:
	pytest -q

commit:
ifndef MSG
	$(error Usage: make commit MSG="your commit message")
endif
	git add -A && git commit -m "$(MSG)"

push:
	git push origin $$(git rev-parse --abbrev-ref HEAD)