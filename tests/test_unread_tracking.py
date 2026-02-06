#!/usr/bin/env python3
"""Tests for the unread tracking, star, and close functionality."""

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
    get_css,
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
    
    def test_bulletin_page_js_keeps_unread_indicator_until_navigation(self):
        """Test that unread indicator stays visible until page navigation.
        
        The JS should mark items as viewed in localStorage but NOT remove
        the 'unread' class immediately - it should stay until the user
        navigates away from the page.
        """
        js = get_bulletin_page_js()
        # Should NOT contain code that removes 'unread' class in the observer
        assert "classList.remove('unread')" not in js
        # Should still mark as viewed in localStorage
        assert "markAsViewed(id)" in js


class TestClickableCards:
    """Tests for clickable card functionality."""
    
    def test_bulletin_card_has_stretched_link_css(self):
        """Test that bulletin cards have CSS for stretched link (entire card clickable)."""
        from generate_site import get_css
        css = get_css()
        # Check for the stretched link pattern using ::after pseudo-element
        assert '.bulletin-card h2 a::after' in css
        assert 'position: absolute' in css
        # Check that the card has cursor pointer
        assert 'cursor: pointer' in css


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


class TestStarFunctionality:
    """Tests for the star functionality."""
    
    def test_star_storage_key_defined(self):
        """Test that starred storage key is defined in JavaScript."""
        js = get_unread_js()
        assert "STARRED_STORAGE_KEY" in js
        assert "bulletin-board-starred" in js
    
    def test_star_functions_exist(self):
        """Test that all required star JavaScript functions are defined."""
        js = get_unread_js()
        assert "function getStarredItems()" in js
        assert "function saveStarredItems(" in js
        assert "function toggleStar(" in js
        assert "function isStarred(" in js
    
    def test_star_button_in_cards(self):
        """Test that star button is added to cards with IDs."""
        lines = [
            "| ID | Event | Date |",
            "|---|---|---|",
            "| event-001 | Concert A | Jan 1 |",
        ]
        html = convert_table_to_html(lines)
        assert 'class="star-btn"' in html
        assert 'title="Star this item"' in html
    
    def test_star_button_not_in_cards_without_id(self):
        """Test that star button is not added to cards without IDs."""
        lines = [
            "| Event | Date |",
            "|---|---|",
            "| Concert A | Jan 1 |",
        ]
        html = convert_table_to_html(lines)
        assert 'class="star-btn"' not in html
    
    def test_starred_css_exists(self):
        """Test that starred item CSS is defined."""
        css = get_css()
        assert '.data-card.starred' in css
        assert '.star-btn' in css
    
    def test_bulletin_page_js_has_star_logic(self):
        """Test that bulletin page JS handles star functionality."""
        js = get_bulletin_page_js()
        assert "isStarred" in js
        assert "toggleStar" in js
        assert "starred" in js
    
    def test_bulletin_page_js_sorts_starred_to_top(self):
        """Test that bulletin page JS sorts starred items to the top."""
        js = get_bulletin_page_js()
        assert "insertBefore" in js
        assert "starredCards" in js


class TestCloseFunctionality:
    """Tests for the close functionality."""
    
    def test_close_storage_key_defined(self):
        """Test that closed storage key is defined in JavaScript."""
        js = get_unread_js()
        assert "CLOSED_STORAGE_KEY" in js
        assert "bulletin-board-closed" in js
    
    def test_close_functions_exist(self):
        """Test that all required close JavaScript functions are defined."""
        js = get_unread_js()
        assert "function getClosedItems()" in js
        assert "function saveClosedItems(" in js
        assert "function closeItem(" in js
        assert "function isClosed(" in js
    
    def test_close_button_in_cards(self):
        """Test that close button is added to cards with IDs."""
        lines = [
            "| ID | Event | Date |",
            "|---|---|---|",
            "| event-001 | Concert A | Jan 1 |",
        ]
        html = convert_table_to_html(lines)
        assert 'class="close-btn"' in html
        assert 'title="Close this item"' in html
    
    def test_close_button_not_in_cards_without_id(self):
        """Test that close button is not added to cards without IDs."""
        lines = [
            "| Event | Date |",
            "|---|---|",
            "| Concert A | Jan 1 |",
        ]
        html = convert_table_to_html(lines)
        assert 'class="close-btn"' not in html
    
    def test_close_css_exists(self):
        """Test that close button CSS is defined."""
        css = get_css()
        assert '.close-btn' in css
    
    def test_bulletin_page_js_has_close_logic(self):
        """Test that bulletin page JS handles close functionality."""
        js = get_bulletin_page_js()
        assert "isClosed" in js
        assert "closeItem" in js
        assert "display = 'none'" in js
    
    def test_closed_items_excluded_from_unread_count(self):
        """Test that closed items are excluded from unread count."""
        js = get_unread_js()
        # The countUnread function should check for closed items
        assert "getClosedItems" in js
        # Verify countUnread uses closedItems
        assert "closedItems" in js


class TestCardActions:
    """Tests for card action buttons."""
    
    def test_card_actions_container_exists(self):
        """Test that card actions container is added to cards with IDs."""
        lines = [
            "| ID | Event | Date |",
            "|---|---|---|",
            "| event-001 | Concert A | Jan 1 |",
        ]
        html = convert_table_to_html(lines)
        assert 'class="card-actions"' in html
    
    def test_card_actions_css_exists(self):
        """Test that card actions CSS is defined."""
        css = get_css()
        assert '.card-actions' in css
        assert 'position: absolute' in css


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
