#!/usr/bin/env python3
"""
Bulletin Board Generator using OpenHands Software Agent SDK.

This script reads a PROMPT.md file from a specified folder and generates/updates
a BULLETIN.md file in the same folder using an AI agent with web search (Tavily),
URL fetching (mcp-server-fetch), and file read/write capabilities.

Usage:
    LLM_API_KEY=<your-api-key> python generate_bulletin.py <folder_path>
    
Example:
    LLM_API_KEY=$CLAUDE_API_KEY TAVILY_API_KEY=$TAVILY_API_KEY python generate_bulletin.py concerts/

Environment Variables:
    LLM_API_KEY      - API key for the LLM (required)
    TAVILY_API_KEY   - API key for Tavily web search (optional but recommended)
    LLM_MODEL        - Model to use (default: anthropic/claude-sonnet-4-5-20250929)
    LLM_BASE_URL     - Custom base URL for the LLM API (optional)
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from pydantic import SecretStr

from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.sdk.logger import get_logger
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool

logger = get_logger(__name__)

META_PROMPT = """You are a Bulletin Board Agent. Your job is to run periodically (e.g., daily) 
to maintain an up-to-date BULLETIN.md file based on a user's interests specified in PROMPT.md.

You have access to powerful web tools:
- **tavily_search**: Search the web for current information (best for finding events, news, etc.)
- **tavily_extract**: Extract content from specific URLs
- **fetch**: Fetch and convert web pages to readable markdown

Your workflow:
1. Read the PROMPT.md file in the target folder to understand what the user is interested in
2. If BULLETIN.md already exists, read it to understand what items are currently listed
3. Use tavily_search to find current, relevant information based on the user's interests
4. Use fetch or tavily_extract to get details from specific venue/event pages
5. Update BULLETIN.md by:
   - Removing stale/outdated items (e.g., events that have already passed)
   - Adding new items or updates you find
   - Keeping items that are still relevant and upcoming
6. Format BULLETIN.md cleanly with:
   - A header indicating this is an auto-generated bulletin
   - The date it was last updated
   - Items organized in a logical way (e.g., by date, category, or relevance)
   - Source links where applicable

Important guidelines:
- Today's date is {today_date}
- Remove any items with dates that have already passed
- Be specific with dates, venues, and details when available
- Include links to sources for verification
- Keep the bulletin concise but informative
- If you can't find information on a topic, mention that in the bulletin
- Prefer tavily_search for discovering new information
- Use fetch for getting full content from known URLs

Start by reading PROMPT.md, then check if BULLETIN.md exists, then search the web for 
relevant information, and finally write the updated BULLETIN.md file.
"""


def build_mcp_config() -> dict:
    """Build MCP configuration for web search and fetch tools."""
    mcp_config: dict = {"mcpServers": {}}
    
    # Add Tavily MCP server if API key is available
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if tavily_api_key:
        mcp_config["mcpServers"]["tavily"] = {
            "command": "uvx",
            "args": ["tavily-mcp"],
            "env": {"TAVILY_API_KEY": tavily_api_key},
        }
        logger.info("Tavily MCP server enabled")
    else:
        logger.warning("TAVILY_API_KEY not set - Tavily search will not be available")
    
    # Add fetch MCP server for URL fetching
    mcp_config["mcpServers"]["fetch"] = {
        "command": "uvx",
        "args": ["mcp-server-fetch"],
    }
    logger.info("Fetch MCP server enabled")
    
    return mcp_config


def run_bulletin_agent(folder_path: str) -> None:
    """Run the bulletin generator agent on the specified folder."""
    folder = Path(folder_path).resolve()
    prompt_file = folder / "PROMPT.md"
    
    if not folder.exists():
        print(f"Error: Folder '{folder}' does not exist.")
        sys.exit(1)
    
    if not prompt_file.exists():
        print(f"Error: PROMPT.md not found in '{folder}'.")
        sys.exit(1)
    
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("Error: LLM_API_KEY environment variable is not set.")
        sys.exit(1)
    
    model = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")
    base_url = os.getenv("LLM_BASE_URL")
    
    llm = LLM(
        model=model,
        api_key=SecretStr(api_key),
        base_url=base_url,
        usage_id="bulletin-agent",
    )
    
    # Core tools for file operations
    tools = [
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
    ]
    
    # Build MCP configuration for web tools
    mcp_config = build_mcp_config()
    
    today_date = datetime.now().strftime("%Y-%m-%d")
    system_prompt = META_PROMPT.format(today_date=today_date)
    
    agent = Agent(
        llm=llm,
        tools=tools,
        mcp_config=mcp_config,
        system_prompt=system_prompt,
    )
    
    conversation = Conversation(
        agent=agent,
        workspace=str(folder),
    )
    
    task_message = f"""Please update the bulletin board for the folder: {folder}

1. Read PROMPT.md to understand what information to gather
2. Check if BULLETIN.md exists and read its current contents
3. Use tavily_search to find current, relevant information on the web
4. Use fetch to get detailed content from specific URLs if needed
5. Write an updated BULLETIN.md with fresh information, removing any stale items

The target folder is: {folder}
Today's date is: {today_date}
"""
    
    print(f"Starting bulletin generator for: {folder}")
    print(f"Using model: {model}")
    print(f"MCP servers: {list(mcp_config['mcpServers'].keys())}")
    print("-" * 50)
    
    conversation.send_message(task_message)
    conversation.run()
    
    print("-" * 50)
    print("Bulletin generation complete!")
    print(f"Cost: ${llm.metrics.accumulated_cost:.4f}")
    
    bulletin_file = folder / "BULLETIN.md"
    if bulletin_file.exists():
        print(f"BULLETIN.md has been updated at: {bulletin_file}")
    else:
        print("Warning: BULLETIN.md was not created.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate/update BULLETIN.md based on PROMPT.md using AI agent"
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing PROMPT.md",
    )
    
    args = parser.parse_args()
    run_bulletin_agent(args.folder)


if __name__ == "__main__":
    main()
