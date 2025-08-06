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

def format_slack_message(msg: dict, user_map: dict[str, str]) -> str:
    """Format Slack message into a readable string with user name."""
    user_id = msg.get("user", "unknown user")
    user_name = user_map.get(user_id, user_id)  # fallback to user ID if name not found
    text = msg.get("text", "")
    ts = msg.get("ts", "")
    return f"[{ts}] {user_name}: {text}"



#Add a helper to build user_id -> name map
async def get_user_name_map() -> dict[str, str]:
    """Fetch and return a mapping of user_id to user name."""
    data = await make_slack_request("users.list")
    if not data or not data.get("ok"):
        return {}
    return {
        user["id"]: user.get("real_name") or user.get("name")
        for user in data["members"]
    }


#get_user_info by Username
@mcp.tool()
async def get_user_info(username: str) -> str:
    """
    Get Slack user info by username or real name.

    Args:
        username: Slack display name or real name (not user ID).
    """
    # Step 1: Get list of all users
    users_data = await make_slack_request("users.list")
    if not users_data or not users_data.get("ok"):
        return "❌ Failed to fetch user list."

    # Step 2: Search for the user
    user_id = None
    for user in users_data["members"]:
        if user.get("name") == username or user.get("real_name") == username:
            user_id = user["id"]
            break

    if not user_id:
        return f"❌ User '{username}' not found."

    # Step 3: Use user_id to get full user info
    params = {"user": user_id}
    data = await make_slack_request("users.info", params)
    if not data or not data.get("ok"):
        return "❌ Failed to fetch user info."

    user = data.get("user", {})
    profile = user.get("profile", {})

    return (
        f"👤 Username: {user.get('name')}\n"
        f"🧾 Real Name: {user.get('real_name')}\n"
        f"📧 Email: {profile.get('email', 'N/A')}\n"
        f"🆔 ID: {user_id}"
    )

#Fetch Messages from a Specific User
@mcp.tool()
async def get_user_messages(channel_id: str, username: str, limit: int = 10) -> str:
    """
    Fetch messages by a specific user (given by name) from a Slack channel.
    
    Args:
        channel_id: The Slack channel ID.
        username: The Slack username or real name of the user.
        limit: How many messages to check (optional).
    """
    # Step 1: Get user list
    users_data = await make_slack_request("users.list")
    if not users_data or not users_data.get("ok"):
        return "❌ Failed to fetch user list."

    # Step 2: Create a user_map and find the user ID
    user_map = {}
    user_id = None
    for user in users_data["members"]:
        uid = user.get("id")
        name = user.get("name")
        real_name = user.get("real_name")

        user_map[uid] = real_name or name or uid

        if name == username or real_name == username:
            user_id = uid

    if not user_id:
        return f"❌ No Slack user found with name '{username}'."

    # Step 3: Fetch channel messages
    params = {"channel": channel_id, "limit": limit}
    data = await make_slack_request("conversations.history", params)

    if not data or not data.get("ok"):
        return "❌ Unable to fetch messages."

    # Step 4: Filter messages by user_id
    user_msgs = [msg for msg in data.get("messages", []) if msg.get("user") == user_id]

    if not user_msgs:
        return f"No messages found from user '{username}' in the channel."

    # ✅ Step 5: Format messages with user_map
    return "\n---\n".join(format_slack_message(msg, user_map) for msg in user_msgs)

#Post Message to a Channel
@mcp.tool()
async def post_message(channel_id: str, text: str) -> str:
    """Post a message to a Slack channel."""
    params = {
        "channel": channel_id,
        "text": text
    }
    data = await make_slack_request("chat.postMessage", params)
    if data and data.get("ok"):
        return "✅ Message posted successfully!"
    return f"❌ Failed to post message. Error: {data.get('error', 'Unknown')}"

# MCP tool: fetch recent messages
@mcp.tool()
async def get_recent_slack_messages(channel_id: str, limit: int = 5) -> str:
    """Fetch recent messages from a Slack channel."""
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

    # 🔁 Get user ID to name map
    user_map = await get_user_name_map()

    # Format with name
    formatted = [
        format_slack_message(msg, user_map) for msg in messages
    ]
    return "\n---\n".join(formatted)


if __name__ == "__main__":
    mcp.run(transport="stdio")
