from fastmcp import FastMCP
import httpx, os, asyncio

mcp = FastMCP("Naver DataLab")

HEADERS = None
BASE = "https://openapi.naver.com"


def init_headers():
    global HEADERS
    if HEADERS is None:
        naver_id = os.getenv("NAVER_CLIENT_ID")
        naver_secret = os.getenv("NAVER_CLIENT_SECRET")
        if not naver_id or not naver_secret:
            raise RuntimeError("NAVER API key is missing.")
        HEADERS = {
            "X-Naver-Client-Id": naver_id,
            "X-Naver-Client-Secret": naver_secret,
        }


@mcp.tool()
async def search_trend(body: dict) -> dict:
    init_headers()
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{BASE}/v1/datalab/search",
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
