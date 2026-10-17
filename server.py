import hashlib
import os

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

EMAIL = "23f3000609@ds.study.iitm.ac.in"

mcp = FastMCP("Exam MCP Server")


@mcp.tool()
def solve_challenge() -> str:
    """Calculate the response using the challenge in the HTTP request header."""
    headers = get_http_headers()
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    normalized_email = EMAIL.strip().lower()
    message = f"{challenge}:{normalized_email}"

    return hashlib.sha256(
        message.encode("utf-8")
    ).hexdigest()[:16]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
