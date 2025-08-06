# Slack-MCP Toolkit 🪤

This project is a **Multi-Tool MCP (Model Context Protocol)** server for Slack automation using the [FastMCP](https://github.com/modelcontextprotocol/fastmcp) library. It allows you to fetch and process Slack messages using AI agents in workflows like Smithery, CrewAI, or MCP Inspector.

---

## 📂 Folder Structure

```
slack-mcp/
├── server.py             # Main MCP tool server with multiple tools
├── utils/
│   └── slack.py          # Contains reusable Slack API functions
├── .env                  # Store your SLACK_TOKEN safely here
├── smithery.yaml         # Configuration for Smithery deployment
├── README.md             # This file
├── video_demo.mp4        # Optional recorded demo
└── requirements.txt      # Python dependencies
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
python server.py
```

2. Use [MCP Inspector](https://inspector.modelcontextprotocol.org/) to call tools and test output

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
pip install -r requirements.txt
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

Never commit this file publicly.

---

## 🎉 Contributing

Pull requests are welcome. If you’d like to add new Slack tools (e.g., `send_message`, `track_reactions`, etc.), feel free to open an issue or PR.

---

## 📹 Video Demo

Check out `video_demo.mp4` for a walkthrough of tool usage in MCP Inspector and Smithery.

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

---

Let me know if you want to add badges, GitHub Actions, or convert this into a proper `mkdocs` site!
