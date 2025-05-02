from fastmcp import FastMCP
import httpx, os

mcp = FastMCP("Naver DataLab")

NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")
HEADERS = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
BASE = "https://openapi.naver.com"

@mcp.tool()
async def search_trend(body: dict) -> dict:
    """
    Naver DataLab 검색어 트렌드 프록시
    """
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/v1/datalab/search",
                              json=body, headers=HEADERS, timeout=30)
    return r.json()

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=80, path="/mcp")
