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
    GOOGLE_API_KEY   - Google API key for agent access (optional)
    LLM_MODEL        - Model to use (default: anthropic/claude-sonnet-4-5-20250929)
    LLM_BASE_URL     - Custom base URL for the LLM API (optional)
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from pydantic import SecretStr

from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.sdk.logger import get_logger
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool

logger = get_logger(__name__)

# Load meta prompt from PROMPT.md file in the same directory as this script
SCRIPT_DIR = Path(__file__).parent
META_PROMPT_FILE = SCRIPT_DIR / "PROMPT.md"
META_PROMPT = META_PROMPT_FILE.read_text()


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
    
    model = os.getenv("LLM_MODEL", "anthropic/claude-opus-4-20250514")
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
    
    agent = Agent(
        llm=llm,
        tools=tools,
        mcp_config=mcp_config,
    )
    
    conversation = Conversation(
        agent=agent,
        workspace=str(folder),
    )
    
    # Add secrets that the agent can access
    secrets = {}
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if google_api_key:
        secrets["GOOGLE_API_KEY"] = google_api_key
        logger.info("GOOGLE_API_KEY secret registered")
    
    if secrets:
        conversation.update_secrets(secrets)
    
    # Use PROMPT.md as the task, not the system prompt
    task_message = META_PROMPT.format(today_date=today_date) + f"""

The target folder is: {folder}
"""
    
    print(f"Starting bulletin generator for: {folder}")
    print(f"Using model: {model}")
    print(f"MCP servers: {list(mcp_config['mcpServers'].keys())}")
    print("-" * 50)
    
    conversation.send_message(task_message)
    conversation.run()
    
    print("-" * 50)
    print("Bulletin generation complete!")
    
    actual_cost = llm.metrics.accumulated_cost
    print(f"Cost: ${actual_cost:.4f}")
    
    bulletin_file = folder / "BULLETIN.md"
    if bulletin_file.exists():
        # Update the cost in frontmatter with the actual cost
        content = bulletin_file.read_text()
        # Match cost field in frontmatter (handles various formats like 0, 0.0, $0.00, etc.)
        updated_content = re.sub(
            r'^(---\n(?:.*\n)*?cost:\s*)\$?[\d.]+',
            rf'\g<1>{actual_cost:.4f}',
            content,
            flags=re.MULTILINE
        )
        bulletin_file.write_text(updated_content)
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
