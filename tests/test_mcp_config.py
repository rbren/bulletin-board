#!/usr/bin/env python3
"""Tests for MCP configuration including Tavily search functionality."""

import os
import sys
from pathlib import Path
from unittest import mock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_bulletin import build_mcp_config


class TestBuildMcpConfig:
    """Tests for the build_mcp_config function."""

    def test_tavily_enabled_when_api_key_set(self):
        """Test that Tavily MCP server is enabled when TAVILY_API_KEY is set."""
        with mock.patch.dict(os.environ, {"TAVILY_API_KEY": "tvly-test-key-123"}):
            config = build_mcp_config()
            
            assert "mcpServers" in config
            assert "tavily" in config["mcpServers"]
            
            tavily_config = config["mcpServers"]["tavily"]
            assert tavily_config["command"] == "uvx"
            assert tavily_config["args"] == ["tavily-mcp"]
            assert tavily_config["env"]["TAVILY_API_KEY"] == "tvly-test-key-123"

    def test_tavily_disabled_when_api_key_not_set(self):
        """Test that Tavily MCP server is not configured when TAVILY_API_KEY is not set."""
        # Ensure TAVILY_API_KEY is not in environment
        env_without_tavily = {k: v for k, v in os.environ.items() if k != "TAVILY_API_KEY"}
        with mock.patch.dict(os.environ, env_without_tavily, clear=True):
            config = build_mcp_config()
            
            assert "mcpServers" in config
            assert "tavily" not in config["mcpServers"]

    def test_fetch_always_enabled(self):
        """Test that fetch MCP server is always enabled regardless of Tavily."""
        # Test with Tavily key
        with mock.patch.dict(os.environ, {"TAVILY_API_KEY": "tvly-test-key"}):
            config = build_mcp_config()
            assert "fetch" in config["mcpServers"]
            assert config["mcpServers"]["fetch"]["command"] == "uvx"
            assert config["mcpServers"]["fetch"]["args"] == ["mcp-server-fetch"]
        
        # Test without Tavily key
        env_without_tavily = {k: v for k, v in os.environ.items() if k != "TAVILY_API_KEY"}
        with mock.patch.dict(os.environ, env_without_tavily, clear=True):
            config = build_mcp_config()
            assert "fetch" in config["mcpServers"]

    def test_mcp_config_structure(self):
        """Test that MCP config has the correct structure."""
        with mock.patch.dict(os.environ, {"TAVILY_API_KEY": "tvly-test-key"}):
            config = build_mcp_config()
            
            # Should have mcpServers key at top level
            assert "mcpServers" in config
            assert isinstance(config["mcpServers"], dict)
            
            # Each server should have command and args
            for server_name, server_config in config["mcpServers"].items():
                assert "command" in server_config, f"{server_name} missing 'command'"
                assert "args" in server_config, f"{server_name} missing 'args'"


class TestPromptContainsTavilyGuidance:
    """Tests to verify the PROMPT.md contains proper Tavily usage guidance."""

    def test_prompt_mentions_tavily_search(self):
        """Test that PROMPT.md mentions tavily_search tool."""
        prompt_file = Path(__file__).parent.parent / "PROMPT.md"
        content = prompt_file.read_text()
        assert "tavily_search" in content

    def test_prompt_mentions_tavily_extract(self):
        """Test that PROMPT.md mentions tavily_extract tool."""
        prompt_file = Path(__file__).parent.parent / "PROMPT.md"
        content = prompt_file.read_text()
        assert "tavily_extract" in content

    def test_prompt_mentions_social_media_access(self):
        """Test that PROMPT.md mentions using Tavily for social media sites."""
        prompt_file = Path(__file__).parent.parent / "PROMPT.md"
        content = prompt_file.read_text()
        # Should mention social media sites that may block direct access
        assert "social media" in content.lower() or "social" in content.lower()

    def test_prompt_mentions_blocked_sites(self):
        """Test that PROMPT.md mentions using Tavily for sites that block agent access."""
        prompt_file = Path(__file__).parent.parent / "PROMPT.md"
        content = prompt_file.read_text()
        # Should mention sites that block access or require authentication
        assert "block" in content.lower() or "authentication" in content.lower()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
