from fastmcp import FastMCP
import httpx, os

mcp = FastMCP("Naver DataLab")


def get_headers():
    nid = os.getenv("NAVER_CLIENT_ID")
    nsec = os.getenv("NAVER_CLIENT_SECRET")
    if not (nid and nsec):
        raise RuntimeError("NAVER API key missing")
    return {"X-Naver-Client-Id": nid, "X-Naver-Client-Secret": nsec}


@mcp.tool()
async def search_trend(body: dict):
    headers = get_headers()
    async with httpx.AsyncClient() as c:
        r = await c.post(
            "https://openapi.naver.com/v1/datalab/search",
            json=body,
            headers=headers,
            timeout=30,
        )
    return r.json()


app = mcp.asgi(path="/mcp")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
