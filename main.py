from fastmcp import FastMCP
import httpx, os, asyncio

mcp = FastMCP("Naver DataLab")

NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")
if not NAVER_ID or not NAVER_SECRET:
    raise RuntimeError("NAVER_CLIENT_ID / NAVER_CLIENT_SECRET is missing")

HEADERS = {
    "X-Naver-Client-Id": NAVER_ID,
    "X-Naver-Client-Secret": NAVER_SECRET,
}
BASE = "https://openapi.naver.com"


@mcp.tool()
async def search_trend(body: dict) -> dict:
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{BASE}/v1/datalab/search", json=body, headers=HEADERS, timeout=30)
    return r.json()


@mcp.tool()
async def shopping_trend(body: dict) -> dict:
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{BASE}/v1/datalab/shopping/categories",
                         json=body, headers=HEADERS, timeout=30)
    return r.json()


if __name__ == "__main__":
    asyncio.run(
        mcp.run(
            transport="sse",
            host="0.0.0.0",
            port=80,
            path="/mcp",
        )
    )
