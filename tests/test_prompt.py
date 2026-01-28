#!/usr/bin/env python3
"""Tests for the PROMPT.md file content."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPromptContent:
    """Tests for the PROMPT.md file content."""
    
    def test_prompt_file_exists(self):
        """Test that PROMPT.md file exists."""
        prompt_file = Path(__file__).parent.parent / "PROMPT.md"
        assert prompt_file.exists(), "PROMPT.md file should exist"
    
    def test_prompt_contains_date_handling_instructions(self):
        """Test that PROMPT.md contains instructions about careful date handling.
        
        The agent should be instructed to use dates from source content
        (e.g., blog post publication dates) rather than the current date.
        """
        prompt_file = Path(__file__).parent.parent / "PROMPT.md"
        content = prompt_file.read_text()
        
        # Check for date handling instructions
        assert "careful about dates" in content.lower(), \
            "PROMPT.md should contain instructions to be careful about dates"
        assert "date from the source" in content.lower() or "date from the post" in content.lower(), \
            "PROMPT.md should instruct to use dates from source content"
    
    def test_prompt_contains_today_date_placeholder(self):
        """Test that PROMPT.md contains the today_date placeholder."""
        prompt_file = Path(__file__).parent.parent / "PROMPT.md"
        content = prompt_file.read_text()
        
        assert "{today_date}" in content, \
            "PROMPT.md should contain {today_date} placeholder"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
