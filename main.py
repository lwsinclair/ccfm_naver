from fastapi import FastAPI
from fastmcp import MCPServer, mcp_tool
import httpx, os

app = FastAPI()
server = MCPServer(app, title="CCFM Naver DataLab MCP")

NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")
headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
base = "https://openapi.naver.com"

@mcp_tool(namespace="datalab", name="search_trend")
async def search_trend(body: dict):
    async with httpx.AsyncClient() as s:
        r = await s.post(f"{base}/v1/datalab/search", json=body, headers=headers, timeout=30)
    return r.json()
