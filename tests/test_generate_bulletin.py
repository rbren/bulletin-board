#!/usr/bin/env python3
"""Tests for bulletin generator MCP configuration."""

import importlib.util
import logging
import os
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "generate_bulletin.py"


class _DummyLLM:
    pass


class _DummyAgent:
    pass


class _DummyConversation:
    pass


class _DummyTool:
    pass


class _DummyFileEditorTool:
    name = "file_editor"


class _DummyTerminalTool:
    name = "terminal"


class BuildMcpConfigTests(unittest.TestCase):
    def load_module(self):
        fake_openhands = types.ModuleType("openhands")
        fake_sdk = types.ModuleType("openhands.sdk")
        fake_sdk.LLM = _DummyLLM
        fake_sdk.Agent = _DummyAgent
        fake_sdk.Conversation = _DummyConversation
        fake_sdk.Tool = _DummyTool

        fake_logger = types.ModuleType("openhands.sdk.logger")
        fake_logger.get_logger = logging.getLogger

        fake_file_editor = types.ModuleType("openhands.tools.file_editor")
        fake_file_editor.FileEditorTool = _DummyFileEditorTool

        fake_terminal = types.ModuleType("openhands.tools.terminal")
        fake_terminal.TerminalTool = _DummyTerminalTool

        fake_pydantic = types.ModuleType("pydantic")
        fake_pydantic.SecretStr = str

        stubbed_modules = {
            "openhands": fake_openhands,
            "openhands.sdk": fake_sdk,
            "openhands.sdk.logger": fake_logger,
            "openhands.tools.file_editor": fake_file_editor,
            "openhands.tools.terminal": fake_terminal,
            "pydantic": fake_pydantic,
        }

        with mock.patch.dict(sys.modules, stubbed_modules):
            spec = importlib.util.spec_from_file_location("generate_bulletin_under_test", MODULE_PATH)
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
        return module

    def test_uses_remote_tavily_mcp_server_when_api_key_is_set(self):
        module = self.load_module()

        with mock.patch.dict(os.environ, {"TAVILY_API_KEY": "test-api-key"}, clear=False):
            config = module.build_mcp_config()

        self.assertEqual(config["mcpServers"]["tavily"], {
            "url": "https://mcp.tavily.com/mcp",
            "api_key": "test-api-key",
        })

    def test_omits_tavily_server_when_api_key_is_missing(self):
        module = self.load_module()

        with mock.patch.dict(os.environ, {}, clear=True):
            config = module.build_mcp_config()

        self.assertNotIn("tavily", config["mcpServers"])
        self.assertEqual(config["mcpServers"]["fetch"], {
            "command": "uvx",
            "args": ["mcp-server-fetch"],
        })


if __name__ == "__main__":
    unittest.main()
