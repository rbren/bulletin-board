#!/usr/bin/env python3
"""Tests for the unread tracking functionality."""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_site import (
    extract_item_ids,
    convert_table_to_html,
    generate_index_page,
    generate_bulletin_page,
    find_bulletins,
    Bulletin,
    get_unread_js,
    get_index_page_js,
    get_bulletin_page_js,
)


class TestExtractItemIds:
    """Tests for the extract_item_ids function."""
    
    def test_extract_ids_from_simple_table(self):
        """Test extracting IDs from a simple markdown table."""
        content = """
| ID | Event | Date |
|---|---|---|
| event-001 | Concert A | Jan 1 |
| event-002 | Concert B | Jan 2 |
"""
        ids = extract_item_ids(content)
        assert ids == ["event-001", "event-002"]
    
    def test_extract_ids_with_id_not_first_column(self):
        """Test extracting IDs when ID column is not first."""
        content = """
| Event | ID | Date |
|---|---|---|
| Concert A | event-001 | Jan 1 |
| Concert B | event-002 | Jan 2 |
"""
        ids = extract_item_ids(content)
        assert ids == ["event-001", "event-002"]
    
    def test_extract_ids_no_id_column(self):
        """Test that no IDs are extracted when there's no ID column."""
        content = """
| Event | Date |
|---|---|
| Concert A | Jan 1 |
| Concert B | Jan 2 |
"""
        ids = extract_item_ids(content)
        assert ids == []
    
    def test_extract_ids_empty_content(self):
        """Test extracting IDs from empty content."""
        ids = extract_item_ids("")
        assert ids == []
    
    def test_extract_ids_no_tables(self):
        """Test extracting IDs from content without tables."""
        content = """
# Heading

Some paragraph text.

- List item 1
- List item 2
"""
        ids = extract_item_ids(content)
        assert ids == []
    
    def test_extract_ids_multiple_tables(self):
        """Test extracting IDs from multiple tables."""
        content = """
## Section 1

| ID | Event |
|---|---|
| id-1 | Event 1 |
| id-2 | Event 2 |

## Section 2

| ID | Story |
|---|---|
| id-3 | Story 1 |
"""
        ids = extract_item_ids(content)
        assert ids == ["id-1", "id-2", "id-3"]


class TestConvertTableToHtml:
    """Tests for the convert_table_to_html function."""
    
    def test_data_id_attribute_added(self):
        """Test that data-id attribute is added to cards."""
        lines = [
            "| ID | Event | Date |",
            "|---|---|---|",
            "| event-001 | Concert A | Jan 1 |",
            "| event-002 | Concert B | Jan 2 |",
        ]
        html = convert_table_to_html(lines)
        assert 'data-id="event-001"' in html
        assert 'data-id="event-002"' in html
    
    def test_id_column_not_displayed(self):
        """Test that ID column content is not displayed in the card."""
        lines = [
            "| ID | Event | Date |",
            "|---|---|---|",
            "| event-001 | Concert A | Jan 1 |",
        ]
        html = convert_table_to_html(lines)
        # ID should be in data attribute but not as visible text
        assert 'data-id="event-001"' in html
        # The ID value should not appear as a field value
        assert '<span class="field-value">event-001</span>' not in html
    
    def test_no_id_column(self):
        """Test table without ID column still works."""
        lines = [
            "| Event | Date |",
            "|---|---|",
            "| Concert A | Jan 1 |",
        ]
        html = convert_table_to_html(lines)
        assert 'class="data-card"' in html
        assert 'data-id=' not in html


class TestGenerateIndexPage:
    """Tests for the generate_index_page function."""
    
    def test_item_ids_in_data_attribute(self):
        """Test that item IDs are included in bulletin card data attributes."""
        bulletins = [
            Bulletin(
                name="test-bulletin",
                title="Test Bulletin",
                path=Path("/test"),
                content="",
                item_ids=["id-1", "id-2", "id-3"]
            )
        ]
        html = generate_index_page(bulletins)
        # Check that data-item-ids attribute exists with JSON-encoded IDs
        assert 'data-item-ids="' in html
        assert '&quot;id-1&quot;' in html
        assert '&quot;id-2&quot;' in html
        assert '&quot;id-3&quot;' in html
    
    def test_javascript_included(self):
        """Test that unread tracking JavaScript is included."""
        bulletins = []
        html = generate_index_page(bulletins)
        assert '<script>' in html
        assert 'countUnread' in html
        assert 'unread-badge' in html
        assert 'localStorage' in html


class TestGenerateBulletinPage:
    """Tests for the generate_bulletin_page function."""
    
    def test_javascript_included(self):
        """Test that unread tracking JavaScript is included."""
        bulletin = Bulletin(
            name="test",
            title="Test",
            path=Path("/test"),
            content="# Test\n\nSome content"
        )
        html = generate_bulletin_page(bulletin)
        assert '<script>' in html
        assert 'IntersectionObserver' in html
        assert 'markAsViewed' in html
        assert 'localStorage' in html


class TestUnreadCss:
    """Tests for unread-related CSS."""
    
    def test_unread_badge_css_exists(self):
        """Test that unread badge CSS is defined."""
        from generate_site import get_css
        css = get_css()
        assert '.unread-badge' in css
    
    def test_unread_item_css_exists(self):
        """Test that unread item CSS is defined."""
        from generate_site import get_css
        css = get_css()
        assert '.data-card.unread' in css


class TestUnreadJavaScript:
    """Tests for unread tracking JavaScript functions."""
    
    def test_storage_key_defined(self):
        """Test that storage key is defined in JavaScript."""
        js = get_unread_js()
        assert "STORAGE_KEY" in js
        assert "bulletin-board-viewed" in js
    
    def test_three_months_constant(self):
        """Test that 3-month cleanup constant is defined."""
        js = get_unread_js()
        assert "THREE_MONTHS_MS" in js
        assert "90" in js  # 90 days
    
    def test_required_functions_exist(self):
        """Test that all required JavaScript functions are defined."""
        js = get_unread_js()
        assert "function getViewedItems()" in js
        assert "function saveViewedItems(" in js
        assert "function cleanupOldEntries()" in js
        assert "function markAsViewed(" in js
        assert "function isViewed(" in js
        assert "function countUnread(" in js
    
    def test_index_page_js_has_badge_logic(self):
        """Test that index page JS creates unread badges."""
        js = get_index_page_js()
        assert "unread-badge" in js
        assert "countUnread" in js
        assert "data-item-ids" in js
    
    def test_bulletin_page_js_has_observer(self):
        """Test that bulletin page JS uses IntersectionObserver."""
        js = get_bulletin_page_js()
        assert "IntersectionObserver" in js
        assert "markAsViewed" in js
        assert "threshold" in js


class TestIntegration:
    """Integration tests for the full site generation."""
    
    def test_find_bulletins_extracts_item_ids(self):
        """Test that find_bulletins extracts item IDs from bulletins."""
        bulletins_dir = Path(__file__).parent.parent / "bulletins"
        if bulletins_dir.exists():
            bulletins = find_bulletins(bulletins_dir)
            # At least one bulletin should have item IDs
            bulletins_with_ids = [b for b in bulletins if b.item_ids]
            assert len(bulletins_with_ids) > 0, "Expected at least one bulletin with item IDs"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
