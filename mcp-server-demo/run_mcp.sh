#!/bin/bash
source /home/deglanrivas/Escritorio/JNE_DCGI/mcp_demo/mcp-server-demo/.venv/bin/activate
uv run --with mcp[cli] mcp run /home/deglanrivas/Escritorio/JNE_DCGI/mcp_demo/mcp-server-demo/main.py
