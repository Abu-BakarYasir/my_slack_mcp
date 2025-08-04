# slack_mcp.py

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
load_dotenv()
SLACK_TOKEN = os.getenv("SLACK_TOKEN")

# Initialize FastMCP server
PORT = os.environ.get("PORT", 10000)
mcp = FastMCP("slack", host="0.0.0.0", port=PORT)

# Slack constants # <-- replace with real token or load from env
SLACK_API_BASE = "https://slack.com/api"

# Helper function to make Slack API request
async def make_slack_request(method: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Make a request to the Slack Web API with proper error handling."""
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SLACK_API_BASE}/{method}", data=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Slack API error: {e}")
            return None

def format_slack_message(msg: dict) -> str:
    """Format Slack message into a readable string."""
    user = msg.get("user", "unknown user")
    text = msg.get("text", "")
    ts = msg.get("ts", "")
    return f"[{ts}] {user}: {text}"

# MCP tool: fetch recent messages
@mcp.tool()
async def get_recent_slack_messages(channel_id: str, limit: int = 5) -> str:
    """Fetch recent messages from a Slack channel.
    
    Args:
        channel_id: The ID of the Slack channel
        limit: Number of recent messages to fetch
    """
    params = {
        "channel": channel_id,
        "limit": limit
    }
    data = await make_slack_request("conversations.history", params)

    if not data or not data.get("ok"):
        return "Unable to fetch Slack messages."

    messages = data.get("messages", [])
    if not messages:
        return "No messages found in the channel."

    formatted = [format_slack_message(msg) for msg in messages]
    return "\n---\n".join(formatted)


if __name__ == "__main__":
    mcp.run(transport="stdio")
