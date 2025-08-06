# Slack-MCP  

This project is a **Multi-Tool MCP (Model Context Protocol)** server for Slack automation using the [FastMCP](https://github.com/modelcontextprotocol/fastmcp) library. It allows you to fetch and process Slack messages using AI agents.This project is great example to learn and Build Understanding reagarding MCPs.

---

## 📂 Folder Structure

```
slack-mcp/
├── main.py               # Main MCP tool server with multiple tools
├── .env                  # Store your SLACK_TOKEN safely here
├── smithery.yaml         # Configuration for Smithery deployment
├── README.md             # This file
├── uv-lock
└── pyproject.toml        # Python dependencies

```

---

## 🚀 Tools in This MCP

### 1. `get_recent_messages`

Fetches the most recent messages from a given Slack channel.

* **Inputs**: `channel_id`, `limit`
* **Returns**: Formatted recent messages.

### 2. `get_user_messages`

Fetches messages from a specific user within a channel.

* **Inputs**: `channel_id`, `username`, `limit`
* **Returns**: Messages sent by the user.

### 3. `summarize_recent_messages`

Summarizes the last N messages from a channel using a connected LLM.

* **Inputs**: `channel_id`, `limit`
* **Returns**: AI-generated summary.

### 4. `group_messages_by_user`

Groups recent channel messages by sender.

* **Inputs**: `channel_id`, `limit`
* **Returns**: A grouped format like:

  ```
  @user1:
  - Message 1
  - Message 2

  @user2:
  - Message A
  ```

---

## 🚪 Slack OAuth Setup & Token Generation

### 1. Create a Slack App

* Go to: [https://api.slack.com/apps](https://api.slack.com/apps)
* Click **Create New App** > From Scratch
* Give it a name and choose your workspace

### 2. Set OAuth Scopes

In **OAuth & Permissions**, under `Bot Token Scopes`, add:

* `channels:read`
* `channels:history`
* `users:read`
* `chat:write` *(optional for sending messages)*

### 3. Install to Workspace

* Click **Install App to Workspace**
* Authorize permissions
* Copy the **Bot User OAuth Token** (starts with `xoxb-...`)

### 4. Save the Token

Create a `.env` file:

```bash
SLACK_TOKEN=xoxb-your-token-here
```

If you change scopes later:

* Revisit **OAuth & Permissions**
* Click **Reinstall App** to apply new scopes

---

## ✨ Testing the Tools

### On MCP Inspector (Local)

1. Run the server:

```bash
python main.py
```

2. Use [MCP Inspector](https://inspector.modelcontextprotocol.org/) to call tools and test output
```bash
mcp dev main.py
```   

### On Smithery (Cloud)

1. Push your code to GitHub
2. Deploy your MCP to Smithery
3. Use the "Run tool" tab to test individual tools

### On Claude (Cloud Desktop)

You can connect these tools via Smithery to Claude workflows for real-time Slack insights and summaries.

---

## 🚜 Requirements

Install dependencies with:

```bash
uv pip install -r pyproject.toml
```

Or manually:

```bash
pip install fastmcp httpx python-dotenv
```

---

## 🔧 Environment File (.env)

```bash
SLACK_TOKEN=xoxb-123-your-token
```



## 🎉 Contributing

Pull requests are welcome. If you’d like to add new Slack tools (e.g., `send_message`, `track_reactions`, etc.), feel free to open an issue or PR.

---

## 📹 Video Demo On claude desktop:



https://github.com/user-attachments/assets/37d905a5-6382-40ce-9500-2dd744656546



---

## 🙏 Acknowledgments

* [FastMCP](https://github.com/modelcontextprotocol/fastmcp) by Model Context Protocol
* [Smithery.ai](https://smithery.ai) for deploying and testing MCPs
* Slack Web API Docs: [https://api.slack.com/](https://api.slack.com/)

---

## 📊 Example Output

> Grouped Slack Messages:

```
@bakar:
- Just pushed latest PR
- Working on the backend API

@hamza:
- Updated Figma designs
- Fixed navbar bug
```

## 📊 Smithery.ai (Cloud Deployment)
Here is the URL go and checkout this mcp_server:
[Slack_MCP_Server](https://smithery.ai/server/@Abu-BakarYasir/my_slack_mcp)

---
## 🧑‍💻 Author

Built by [Abu Bakar Yasir](https://github.com/Abu-BakarYasir) — Computer Engineering @ COMSATS + AI Software Engineer | Full Stack Developer 🚀


