# Bulletin Board Repository

An automated bulletin board system that uses OpenHands AI agents to regularly gather and update information based on user-defined interests.

## Overview

This repository contains a Python script that leverages the **OpenHands Software Agent SDK** to:
1. Read user interests from a `PROMPT.md` file in a topic folder
2. Search the web for relevant, current information using MCP tools
3. Generate/update a `BULLETIN.md` file with organized, up-to-date content
4. Automatically remove stale items and add new ones

## Repository Structure

```
bulletin-board/
├── generate_bulletin.py          # Main bulletin generator script
├── .github/
│   └── workflows/
│       └── update-bulletins.yml  # GitHub Action for daily updates
├── concerts/                     # Example topic folder
│   ├── PROMPT.md                 # User interests/preferences
│   └── BULLETIN.md               # Auto-generated bulletin (output)
└── .openhands/
    └── skills/
        └── repo.md               # This file
```

## How It Works

### 1. Topic Folders

Each topic (e.g., `concerts/`) contains:
- **`PROMPT.md`**: Describes what the user is interested in (venues, genres, locations, etc.)
- **`BULLETIN.md`**: Auto-generated output with current information

### 2. The Generator Script (`generate_bulletin.py`)

The script uses the OpenHands SDK with MCP (Model Context Protocol) tools:

```python
mcp_config = {
    "mcpServers": {
        "tavily": {"command": "uvx", "args": ["tavily-mcp"], "env": {"TAVILY_API_KEY": "..."}},
        "fetch": {"command": "uvx", "args": ["mcp-server-fetch"]},
    }
}
```

**Available Tools:**
- `tavily_search` - Web search for finding events, news, etc.
- `tavily_extract` - Extract content from specific URLs
- `fetch` - Fetch URLs and convert to markdown
- `file_editor` - Read/write files
- `terminal` - Execute shell commands

### 3. GitHub Action

The workflow (`.github/workflows/update-bulletins.yml`) runs:
- **Daily** at 8 AM UTC (cron schedule)
- **On-demand** via manual workflow_dispatch

It automatically commits and pushes any changes to BULLETIN.md files.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LLM_API_KEY` | Yes | API key for the LLM (Claude) |
| `TAVILY_API_KEY` | Recommended | API key for Tavily web search |
| `LLM_MODEL` | No | Model to use (default: `anthropic/claude-sonnet-4-5-20250929`) |
| `LLM_BASE_URL` | No | Custom base URL for LLM API |

## GitHub Secrets

The repository requires these secrets for the GitHub Action:
- `CLAUDE_API_KEY` - Anthropic API key
- `TAVILY_API_KEY` - Tavily API key

## Usage

### Running Locally

```bash
# Install dependencies
pip install openhands-sdk openhands-tools

# Run the generator
LLM_API_KEY=$CLAUDE_API_KEY TAVILY_API_KEY=$TAVILY_API_KEY python generate_bulletin.py concerts/
```

### Adding a New Topic

1. Create a new folder (e.g., `sports/`)
2. Add a `PROMPT.md` file describing your interests
3. Update the GitHub Action workflow to include the new folder
4. Run the generator or wait for the scheduled run

## Key Dependencies

- **openhands-sdk**: Core agent framework
- **openhands-tools**: Built-in tools (file editor, terminal)
- **tavily-mcp**: MCP server for web search (via uvx)
- **mcp-server-fetch**: MCP server for URL fetching (via uvx)

## Development Notes

- MCP servers are spawned as subprocesses by the SDK via `uvx`
- The agent uses a system prompt that includes the current date for time-aware filtering
- Bulletins include source links for verification
- The agent is instructed to remove past events and prioritize upcoming ones
