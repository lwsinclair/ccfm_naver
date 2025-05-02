from fastmcp import FastMCP
import httpx
import os
from pydantic import BaseModel
from typing import List, Any

# keywordGroups의 구조를 명확히 정의
class KeywordGroup(BaseModel):
    groupName: str
    keywords: List[str]

class SearchTrendRequest(BaseModel):
    startDate: str
    endDate: str
    timeUnit: str
    keywordGroups: List[KeywordGroup]
    device: str = "pc"
    gender: str = "all"
    ages: List[str] = []

# 반환값도 Pydantic 모델로 감싸기
class SearchTrendResponse(BaseModel):
    results: Any

mcp = FastMCP("Naver DataLab")

def get_headers():
    nid = os.getenv("NAVER_CLIENT_ID")
    nsec = os.getenv("NAVER_CLIENT_SECRET")
    if not (nid and nsec):
        raise RuntimeError("NAVER API key missing")
    return {"X-Naver-Client-Id": nid, "X-Naver-Client-Secret": nsec}

@mcp.tool()
async def search_trend(body: SearchTrendRequest) -> SearchTrendResponse:
    headers = get_headers()
    async with httpx.AsyncClient() as c:
        response = await c.post(
            "https://openapi.naver.com/v1/datalab/search",
            json=body.dict(),
            headers=headers,
            timeout=30,
        )
    return SearchTrendResponse(results=response.json())

app = mcp.asgi(path="/mcp")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
