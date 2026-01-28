#!/usr/bin/env python3
"""
Generate a static website from BULLETIN.md files.

This script finds all BULLETIN.md files in the bulletins directory,
converts them to nicely styled HTML pages, and generates an index page.
"""

import json
import os
import re
import shutil
import yaml
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Bulletin:
    """Represents a bulletin with its metadata and content."""
    name: str
    title: str
    path: Path
    content: str
    frontmatter: dict = field(default_factory=dict)
    last_updated: str | None = None
    item_ids: list = field(default_factory=list)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from content. Returns (frontmatter_dict, remaining_content)."""
    if not content.startswith("---"):
        return {}, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}
    
    remaining_content = parts[2].strip()
    return frontmatter, remaining_content


def extract_item_ids(content: str) -> list[str]:
    """Extract item IDs from markdown tables in the content."""
    item_ids = []
    lines = content.split("\n")
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line looks like a table header (has |)
        if "|" in line and i + 1 < len(lines):
            # Check if next line is a separator (contains |---|)
            next_line = lines[i + 1]
            if re.match(r"^\|?[\s\-:|]+\|[\s\-:|]+\|?$", next_line):
                # This is a table - parse headers to find ID column
                def parse_row(row_line: str) -> list[str]:
                    row_line = row_line.strip()
                    if row_line.startswith("|"):
                        row_line = row_line[1:]
                    if row_line.endswith("|"):
                        row_line = row_line[:-1]
                    return [cell.strip() for cell in row_line.split("|")]
                
                headers = parse_row(line)
                id_col_idx = None
                for idx, h in enumerate(headers):
                    if h.lower() == "id":
                        id_col_idx = idx
                        break
                
                # Skip header and separator
                j = i + 2
                
                # Parse data rows
                while j < len(lines) and "|" in lines[j]:
                    if not re.match(r"^[\s\-:|]+$", lines[j]):
                        row = parse_row(lines[j])
                        if id_col_idx is not None and id_col_idx < len(row):
                            item_id = row[id_col_idx].strip()
                            if item_id:
                                item_ids.append(item_id)
                    j += 1
                
                i = j
                continue
        
        i += 1
    
    return item_ids


def find_bulletins(bulletins_dir: Path) -> list[Bulletin]:
    """Find all BULLETIN.md files in the bulletins directory."""
    bulletins = []
    
    for bulletin_file in bulletins_dir.rglob("BULLETIN.md"):
        folder_name = bulletin_file.parent.name
        raw_content = bulletin_file.read_text(encoding="utf-8")
        
        # Parse frontmatter
        frontmatter, content = parse_frontmatter(raw_content)
        
        # Extract title from frontmatter or first H1 heading
        title = frontmatter.get("title", "").replace("-", " ").title()
        if not title:
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1) if title_match else folder_name.replace("-", " ").title()
        
        # Extract last updated date from frontmatter
        last_updated = None
        if "updated_at" in frontmatter:
            updated = frontmatter["updated_at"]
            if hasattr(updated, "strftime"):
                last_updated = updated.strftime("%B %d, %Y")
            else:
                last_updated = str(updated)[:10]
        
        # Extract item IDs from tables
        item_ids = extract_item_ids(content)
        
        bulletins.append(Bulletin(
            name=folder_name,
            title=title,
            path=bulletin_file,
            content=content,
            frontmatter=frontmatter,
            last_updated=last_updated,
            item_ids=item_ids
        ))
    
    return sorted(bulletins, key=lambda b: b.title)


def markdown_to_html(markdown: str) -> str:
    """Convert markdown to HTML with support for common elements."""
    html = markdown
    
    # Escape HTML entities first (except for links which we'll handle)
    html = html.replace("&", "&amp;")
    html = html.replace("<", "&lt;")
    html = html.replace(">", "&gt;")
    
    # Restore markdown syntax that was escaped
    html = html.replace("&gt;", ">")  # Will be handled by blockquotes
    
    # Process code blocks first (to prevent other processing inside them)
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(1))
        return f"<<<CODE_BLOCK_{len(code_blocks) - 1}>>>"
    
    html = re.sub(r"```[\w]*\n(.*?)```", save_code_block, html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    
    # Headers
    html = re.sub(r"^######\s+(.+)$", r"<h6>\1</h6>", html, flags=re.MULTILINE)
    html = re.sub(r"^#####\s+(.+)$", r"<h5>\1</h5>", html, flags=re.MULTILINE)
    html = re.sub(r"^####\s+(.+)$", r"<h4>\1</h4>", html, flags=re.MULTILINE)
    html = re.sub(r"^###\s+(.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^##\s+(.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^#\s+(.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", html)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", html)
    
    # Links
    html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', html)
    
    # Auto-link URLs
    html = re.sub(
        r'(?<!href=")(?<!">)(https?://[^\s<>"\)]+)',
        r'<a href="\1" target="_blank" rel="noopener">\1</a>',
        html
    )
    
    # Horizontal rules
    html = re.sub(r"^---+$", r"<hr>", html, flags=re.MULTILINE)
    
    # Process tables
    html = process_tables(html)
    
    # Lists (unordered)
    def process_list(text):
        lines = text.split("\n")
        result = []
        in_list = False
        list_items = []
        
        for line in lines:
            list_match = re.match(r"^(\s*)[-*]\s+(.+)$", line)
            if list_match:
                if not in_list:
                    in_list = True
                    list_items = []
                list_items.append(f"<li>{list_match.group(2)}</li>")
            else:
                if in_list:
                    result.append("<ul>" + "".join(list_items) + "</ul>")
                    in_list = False
                    list_items = []
                result.append(line)
        
        if in_list:
            result.append("<ul>" + "".join(list_items) + "</ul>")
        
        return "\n".join(result)
    
    html = process_list(html)
    
    # Ordered lists
    def process_ordered_list(text):
        lines = text.split("\n")
        result = []
        in_list = False
        list_items = []
        
        for line in lines:
            list_match = re.match(r"^(\s*)\d+\.\s+(.+)$", line)
            if list_match:
                if not in_list:
                    in_list = True
                    list_items = []
                list_items.append(f"<li>{list_match.group(2)}</li>")
            else:
                if in_list:
                    result.append("<ol>" + "".join(list_items) + "</ol>")
                    in_list = False
                    list_items = []
                result.append(line)
        
        if in_list:
            result.append("<ol>" + "".join(list_items) + "</ol>")
        
        return "\n".join(result)
    
    html = process_ordered_list(html)
    
    # Paragraphs - wrap remaining text blocks
    paragraphs = []
    current_para = []
    
    for line in html.split("\n"):
        stripped = line.strip()
        # Skip if it's an HTML element, empty, or special marker
        if (stripped.startswith("<") and not stripped.startswith("<a ") and not stripped.startswith("<strong") 
            and not stripped.startswith("<em") and not stripped.startswith("<code")):
            if current_para:
                para_text = " ".join(current_para)
                if para_text.strip():
                    paragraphs.append(f"<p>{para_text}</p>")
                current_para = []
            paragraphs.append(line)
        elif stripped == "":
            if current_para:
                para_text = " ".join(current_para)
                if para_text.strip():
                    paragraphs.append(f"<p>{para_text}</p>")
                current_para = []
        elif stripped.startswith("<<<CODE_BLOCK_"):
            if current_para:
                para_text = " ".join(current_para)
                if para_text.strip():
                    paragraphs.append(f"<p>{para_text}</p>")
                current_para = []
            paragraphs.append(line)
        else:
            current_para.append(stripped)
    
    if current_para:
        para_text = " ".join(current_para)
        if para_text.strip():
            paragraphs.append(f"<p>{para_text}</p>")
    
    html = "\n".join(paragraphs)
    
    # Restore code blocks
    for i, code in enumerate(code_blocks):
        html = html.replace(f"<<<CODE_BLOCK_{i}>>>", f"<pre><code>{code}</code></pre>")
    
    return html


def process_tables(html: str) -> str:
    """Convert markdown tables to HTML tables with proper styling."""
    lines = html.split("\n")
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line looks like a table header (has |)
        if "|" in line and i + 1 < len(lines):
            # Check if next line is a separator (contains |---|)
            next_line = lines[i + 1]
            if re.match(r"^\|?[\s\-:|]+\|[\s\-:|]+\|?$", next_line):
                # This is a table - parse it
                table_lines = [line]
                j = i + 1
                
                while j < len(lines) and "|" in lines[j]:
                    table_lines.append(lines[j])
                    j += 1
                
                table_html = convert_table_to_html(table_lines)
                result.append(table_html)
                i = j
                continue
        
        result.append(line)
        i += 1
    
    return "\n".join(result)


def convert_table_to_html(lines: list[str]) -> str:
    """Convert markdown table lines to HTML cards (hiding ID column but using it as data-id)."""
    if len(lines) < 2:
        return "\n".join(lines)
    
    def parse_row(line: str) -> list[str]:
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [cell.strip() for cell in line.split("|")]
    
    headers = parse_row(lines[0])
    rows = [parse_row(line) for line in lines[2:] if not re.match(r"^[\s\-:|]+$", line)]
    
    # Find ID column index to use for data-id attribute
    id_col_idx = None
    for i, h in enumerate(headers):
        if h.lower() == "id":
            id_col_idx = i
            break
    
    # Extract IDs and filter out ID column from display
    row_ids = []
    filtered_headers = [h for i, h in enumerate(headers) if i != id_col_idx]
    filtered_rows = []
    for row in rows:
        row_id = row[id_col_idx] if id_col_idx is not None and id_col_idx < len(row) else None
        row_ids.append(row_id)
        filtered_rows.append([cell for i, cell in enumerate(row) if i != id_col_idx])
    
    # Build card-based HTML
    html = ['<div class="cards-container">']
    
    for idx, row in enumerate(filtered_rows):
        row_id = row_ids[idx]
        data_id_attr = f' data-id="{row_id}"' if row_id else ''
        html.append(f'<div class="data-card"{data_id_attr}>')
        
        # Add action buttons (star and close) if the card has an ID
        if row_id:
            html.append('<div class="card-actions">')
            html.append('<button class="star-btn" title="Star this item">☆</button>')
            html.append('<button class="close-btn" title="Close this item">×</button>')
            html.append('</div>')
        
        for i, cell in enumerate(row):
            if i < len(filtered_headers):
                header = filtered_headers[i]
                # Special handling for Link columns
                if header.lower() == "link" and cell:
                    html.append(f'<div class="card-field card-link">{cell}</div>')
                # Special handling for title/event/story columns - make them prominent
                elif header.lower() in ("event", "story", "title"):
                    html.append(f'<div class="card-title">{cell}</div>')
                else:
                    html.append(f'<div class="card-field"><span class="field-label">{header}</span><span class="field-value">{cell}</span></div>')
        html.append('</div>')
    
    html.append('</div>')
    return "\n".join(html)


def get_css() -> str:
    """Return the CSS for the website."""
    return """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-color: #0f0f1a;
    --bg-gradient: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    --card-bg: rgba(30, 32, 48, 0.8);
    --card-bg-hover: rgba(40, 44, 66, 0.9);
    --text-color: #e2e8f0;
    --text-muted: #94a3b8;
    --heading-color: #f8fafc;
    --accent-color: #818cf8;
    --accent-hover: #a5b4fc;
    --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --link-color: #60a5fa;
    --border-color: rgba(148, 163, 184, 0.15);
    --success-color: #34d399;
    --warning-color: #fbbf24;
    --glass-border: rgba(255, 255, 255, 0.1);
    --shadow-color: rgba(0, 0, 0, 0.3);
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-gradient);
    background-attachment: fixed;
    color: var(--text-color);
    line-height: 1.7;
    min-height: 100vh;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem;
}

/* Header styles */
header {
    text-align: center;
    padding: 4rem 0 3rem;
    margin-bottom: 3rem;
    position: relative;
}

header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 2px;
    background: var(--accent-gradient);
    border-radius: 2px;
}

header h1 {
    color: var(--heading-color);
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

header p {
    color: var(--text-muted);
    font-size: 1.15rem;
    font-weight: 400;
}

/* Back link */
.back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--accent-color);
    text-decoration: none;
    margin-bottom: 2rem;
    font-size: 0.95rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    background: rgba(129, 140, 248, 0.1);
    transition: all 0.3s ease;
}

.back-link:hover {
    color: var(--accent-hover);
    background: rgba(129, 140, 248, 0.2);
    transform: translateX(-4px);
}

/* Bulletin list on index page */
.bulletin-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.bulletin-card {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 1.75rem;
    border: 1px solid var(--glass-border);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.bulletin-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--accent-gradient);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.bulletin-card:hover {
    transform: translateY(-4px);
    background: var(--card-bg-hover);
    box-shadow: 0 20px 40px var(--shadow-color);
}

.bulletin-card:hover::before {
    opacity: 1;
}

.bulletin-card h2 {
    color: var(--heading-color);
    font-size: 1.35rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.bulletin-card h2 a {
    color: inherit;
    text-decoration: none;
    transition: color 0.2s ease;
}

/* Make the entire card clickable by stretching the link */
.bulletin-card h2 a::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1;
}

.bulletin-card h2 a:hover {
    color: var(--accent-color);
}

.bulletin-card {
    cursor: pointer;
}

.bulletin-card .meta {
    color: var(--text-muted);
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.bulletin-card .meta::before {
    content: '🕐';
    font-size: 0.8rem;
}

/* Metadata section */
.metadata-section {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
}

.metadata-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.metadata-item .label {
    color: var(--text-muted);
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metadata-item .value {
    color: var(--heading-color);
    font-weight: 600;
}

/* Article content */
article {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2.5rem;
    border: 1px solid var(--glass-border);
    box-shadow: 0 10px 40px var(--shadow-color);
}

article h1 {
    color: var(--heading-color);
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
    letter-spacing: -0.02em;
}

article h2 {
    color: var(--heading-color);
    font-size: 1.5rem;
    font-weight: 600;
    margin: 2.5rem 0 1rem;
}

article h3 {
    color: var(--heading-color);
    font-size: 1.25rem;
    font-weight: 600;
    margin: 2rem 0 0.75rem;
}

article h4, article h5, article h6 {
    color: var(--heading-color);
    font-weight: 600;
    margin: 1.5rem 0 0.5rem;
}

article p {
    margin: 1rem 0;
    line-height: 1.8;
}

article a {
    color: var(--link-color);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
    border-bottom: 1px solid transparent;
}

article a:hover {
    color: var(--accent-hover);
    border-bottom-color: var(--accent-hover);
}

article ul, article ol {
    margin: 1rem 0;
    padding-left: 1.5rem;
}

article li {
    margin: 0.5rem 0;
}

article hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: 2.5rem 0;
}

article strong {
    color: var(--heading-color);
    font-weight: 600;
}

article code {
    background: rgba(129, 140, 248, 0.15);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-size: 0.9em;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    color: var(--accent-color);
}

article pre {
    background: rgba(15, 15, 26, 0.8);
    padding: 1.25rem;
    border-radius: 12px;
    overflow-x: auto;
    margin: 1.5rem 0;
    border: 1px solid var(--border-color);
}

article pre code {
    background: none;
    padding: 0;
    color: var(--text-color);
}

/* Data Cards (replaces tables) */
.cards-container {
    display: grid;
    gap: 1rem;
    margin: 1.5rem 0;
}

.data-card {
    background: rgba(15, 15, 26, 0.5);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    transition: all 0.3s ease;
}

.data-card:hover {
    background: rgba(30, 32, 48, 0.6);
    border-color: rgba(129, 140, 248, 0.3);
    transform: translateX(4px);
}

.card-title {
    color: var(--heading-color);
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    line-height: 1.4;
}

.card-field {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    align-items: baseline;
}

.card-field:last-child {
    margin-bottom: 0;
}

.field-label {
    color: var(--text-muted);
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    min-width: 80px;
}

.field-value {
    color: var(--text-color);
    flex: 1;
}

.card-link {
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border-color);
}

.card-link a {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    color: var(--accent-color);
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.4rem 0.75rem;
    background: rgba(129, 140, 248, 0.1);
    border-radius: 6px;
    transition: all 0.2s ease;
}

.card-link a:hover {
    background: rgba(129, 140, 248, 0.2);
    color: var(--accent-hover);
    border-bottom: none;
}

.card-link a::after {
    content: '→';
}

/* Legacy table styles (kept for fallback) */
.table-wrapper {
    overflow-x: auto;
    margin: 1.5rem 0;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
}

th {
    background: rgba(15, 15, 26, 0.8);
    color: var(--heading-color);
    font-weight: 600;
    text-align: left;
    padding: 1rem;
    border-bottom: 2px solid var(--border-color);
}

td {
    padding: 0.875rem 1rem;
    border-bottom: 1px solid var(--border-color);
}

tr:nth-child(even) {
    background: rgba(30, 32, 48, 0.3);
}

tr:last-child td {
    border-bottom: none;
}

/* Footer */
footer {
    text-align: center;
    padding: 2.5rem 0;
    margin-top: 3rem;
    color: var(--text-muted);
    font-size: 0.9rem;
    position: relative;
}

footer::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
    
    header {
        padding: 2.5rem 0 2rem;
    }
    
    header h1 {
        font-size: 2rem;
    }
    
    .bulletin-list {
        grid-template-columns: 1fr;
    }
    
    article {
        padding: 1.5rem;
        border-radius: 16px;
    }
    
    article h1 {
        font-size: 1.5rem;
    }
    
    .metadata-section {
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .data-card {
        padding: 1rem;
    }
    
    .field-label {
        min-width: 70px;
    }
}

/* Unread badge styles */
.unread-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-gradient);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    min-width: 20px;
    height: 20px;
    padding: 0 6px;
    border-radius: 10px;
    margin-left: 8px;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
}

.bulletin-card h2 {
    display: flex;
    align-items: center;
}

/* Unread item highlight */
.data-card.unread {
    border: 2px solid var(--accent-color);
    box-shadow: 0 0 20px rgba(129, 140, 248, 0.3);
}

.data-card.unread::before {
    content: 'NEW';
    position: absolute;
    top: 8px;
    right: 70px;
    background: var(--accent-gradient);
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    letter-spacing: 0.05em;
}

/* Card action buttons (star and close) */
.card-actions {
    position: absolute;
    top: 8px;
    right: 8px;
    display: flex;
    gap: 4px;
    z-index: 10;
}

.star-btn, .close-btn {
    background: rgba(30, 32, 48, 0.8);
    border: 1px solid var(--glass-border);
    color: var(--text-muted);
    width: 28px;
    height: 28px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

.star-btn:hover {
    background: rgba(251, 191, 36, 0.2);
    border-color: var(--warning-color);
    color: var(--warning-color);
}

.close-btn:hover {
    background: rgba(239, 68, 68, 0.2);
    border-color: #ef4444;
    color: #ef4444;
}

/* Starred item styles */
.data-card.starred {
    border: 2px solid var(--warning-color);
    box-shadow: 0 0 20px rgba(251, 191, 36, 0.2);
}

.data-card.starred .star-btn {
    background: rgba(251, 191, 36, 0.3);
    border-color: var(--warning-color);
    color: var(--warning-color);
}

.data-card.starred .star-btn::after {
    content: '★';
    position: absolute;
}

.data-card.starred .star-btn {
    color: transparent;
}

.data-card.starred .star-btn::after {
    color: var(--warning-color);
}

/* Adjust unread badge position when card has actions */
.data-card.starred.unread::before {
    border-color: var(--warning-color);
}
"""


def get_unread_js() -> str:
    """Return the JavaScript for tracking unread items."""
    return """
const STORAGE_KEY = 'bulletin-board-viewed';
const STARRED_STORAGE_KEY = 'bulletin-board-starred';
const CLOSED_STORAGE_KEY = 'bulletin-board-closed';
const THREE_MONTHS_MS = 90 * 24 * 60 * 60 * 1000;

function getViewedItems() {
    try {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : {};
    } catch (e) {
        return {};
    }
}

function saveViewedItems(items) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    } catch (e) {
        console.warn('Could not save to localStorage:', e);
    }
}

function cleanupOldEntries() {
    const items = getViewedItems();
    const now = Date.now();
    let changed = false;
    
    for (const id in items) {
        if (now - items[id] > THREE_MONTHS_MS) {
            delete items[id];
            changed = true;
        }
    }
    
    if (changed) {
        saveViewedItems(items);
    }
    
    return items;
}

function markAsViewed(id) {
    const items = getViewedItems();
    if (!items[id]) {
        items[id] = Date.now();
        saveViewedItems(items);
    }
}

function isViewed(id) {
    const items = getViewedItems();
    return !!items[id];
}

function countUnread(itemIds) {
    const items = getViewedItems();
    const closedItems = getClosedItems();
    return itemIds.filter(id => !items[id] && !closedItems[id]).length;
}

// Star functionality
function getStarredItems() {
    try {
        const data = localStorage.getItem(STARRED_STORAGE_KEY);
        return data ? JSON.parse(data) : {};
    } catch (e) {
        return {};
    }
}

function saveStarredItems(items) {
    try {
        localStorage.setItem(STARRED_STORAGE_KEY, JSON.stringify(items));
    } catch (e) {
        console.warn('Could not save starred items to localStorage:', e);
    }
}

function toggleStar(id) {
    const items = getStarredItems();
    if (items[id]) {
        delete items[id];
    } else {
        items[id] = Date.now();
    }
    saveStarredItems(items);
    return !!items[id];
}

function isStarred(id) {
    const items = getStarredItems();
    return !!items[id];
}

// Close functionality
function getClosedItems() {
    try {
        const data = localStorage.getItem(CLOSED_STORAGE_KEY);
        return data ? JSON.parse(data) : {};
    } catch (e) {
        return {};
    }
}

function saveClosedItems(items) {
    try {
        localStorage.setItem(CLOSED_STORAGE_KEY, JSON.stringify(items));
    } catch (e) {
        console.warn('Could not save closed items to localStorage:', e);
    }
}

function closeItem(id) {
    const items = getClosedItems();
    items[id] = Date.now();
    saveClosedItems(items);
}

function isClosed(id) {
    const items = getClosedItems();
    return !!items[id];
}
"""


def get_index_page_js() -> str:
    """Return the JavaScript for the index page to show unread badges."""
    return get_unread_js() + """
document.addEventListener('DOMContentLoaded', function() {
    cleanupOldEntries();
    
    document.querySelectorAll('.bulletin-card').forEach(function(card) {
        const itemIdsAttr = card.getAttribute('data-item-ids');
        if (itemIdsAttr) {
            try {
                const itemIds = JSON.parse(itemIdsAttr);
                const unreadCount = countUnread(itemIds);
                
                if (unreadCount > 0) {
                    const badge = document.createElement('span');
                    badge.className = 'unread-badge';
                    badge.textContent = unreadCount;
                    const h2 = card.querySelector('h2');
                    if (h2) {
                        h2.appendChild(badge);
                    }
                }
            } catch (e) {
                console.warn('Could not parse item IDs:', e);
            }
        }
    });
});
"""


def get_bulletin_page_js() -> str:
    """Return the JavaScript for bulletin pages to track viewed items."""
    return get_unread_js() + """
document.addEventListener('DOMContentLoaded', function() {
    cleanupOldEntries();
    
    const cards = document.querySelectorAll('.data-card[data-id]');
    
    // Hide closed items and mark starred/unread items
    cards.forEach(function(card) {
        const id = card.getAttribute('data-id');
        if (id) {
            if (isClosed(id)) {
                card.style.display = 'none';
            } else {
                if (isStarred(id)) {
                    card.classList.add('starred');
                }
                if (!isViewed(id)) {
                    card.classList.add('unread');
                }
            }
        }
    });
    
    // Sort starred items to the top within each cards-container
    document.querySelectorAll('.cards-container').forEach(function(container) {
        const cardsInContainer = Array.from(container.querySelectorAll('.data-card[data-id]'));
        const starredCards = cardsInContainer.filter(function(card) {
            return card.classList.contains('starred');
        });
        
        // Move starred cards to the top
        starredCards.forEach(function(card) {
            container.insertBefore(card, container.firstChild);
        });
    });
    
    // Set up star button click handlers
    document.querySelectorAll('.star-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const card = btn.closest('.data-card');
            const id = card.getAttribute('data-id');
            if (id) {
                const nowStarred = toggleStar(id);
                if (nowStarred) {
                    card.classList.add('starred');
                } else {
                    card.classList.remove('starred');
                }
            }
        });
    });
    
    // Set up close button click handlers
    document.querySelectorAll('.close-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const card = btn.closest('.data-card');
            const id = card.getAttribute('data-id');
            if (id) {
                closeItem(id);
                card.style.display = 'none';
            }
        });
    });
    
    // Set up IntersectionObserver to track when items are viewed
    // Note: We mark items as viewed in localStorage but keep the visual indicator
    // until the user navigates away from the page
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const card = entry.target;
                const id = card.getAttribute('data-id');
                if (id) {
                    markAsViewed(id);
                    // Don't remove 'unread' class - keep visual indicator until page navigation
                }
            }
        });
    }, {
        threshold: 0.5  // Item must be 50% visible
    });
    
    cards.forEach(function(card) {
        observer.observe(card);
    });
});
"""


def generate_index_page(bulletins: list[Bulletin]) -> str:
    """Generate the index page HTML."""
    bulletin_cards = []
    for b in bulletins:
        meta = f"Last updated: {b.last_updated}" if b.last_updated else ""
        # Encode item IDs as JSON for the data attribute
        item_ids_json = json.dumps(b.item_ids).replace('"', '&quot;')
        bulletin_cards.append(f"""
        <div class="bulletin-card" data-item-ids="{item_ids_json}">
            <h2><a href="{b.name}.html">{b.title}</a></h2>
            <p class="meta">{meta}</p>
        </div>
        """)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bulletin Board</title>
    <style>{get_css()}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 Bulletin Board</h1>
            <p>Auto-generated bulletins on things I care about</p>
        </header>
        
        <main>
            <div class="bulletin-list">
                {"".join(bulletin_cards)}
            </div>
        </main>
        
        <footer>
            <p>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}</p>
        </footer>
    </div>
    <script>{get_index_page_js()}</script>
</body>
</html>
"""


def generate_metadata_html(frontmatter: dict) -> str:
    """Generate HTML for the metadata section from frontmatter."""
    if not frontmatter:
        return ""
    
    items = []
    
    # Display specific metadata fields with nice formatting
    if "updated_at" in frontmatter:
        updated = frontmatter["updated_at"]
        if hasattr(updated, "strftime"):
            date_str = updated.strftime("%B %d, %Y")
        else:
            date_str = str(updated)[:10]
        items.append(f'<div class="metadata-item"><span class="label">📅 Updated</span><span class="value">{date_str}</span></div>')
    
    if "cost" in frontmatter:
        cost = frontmatter["cost"]
        if cost == 0:
            cost_str = "Free"
        else:
            cost_str = f"${cost}"
        items.append(f'<div class="metadata-item"><span class="label">💰 Cost</span><span class="value">{cost_str}</span></div>')
    
    # Add any other metadata fields
    skip_keys = {"title", "updated_at", "cost"}
    for key, value in frontmatter.items():
        if key not in skip_keys and value is not None:
            items.append(f'<div class="metadata-item"><span class="label">{key.replace("_", " ").title()}</span><span class="value">{value}</span></div>')
    
    if not items:
        return ""
    
    return f'<div class="metadata-section">{"".join(items)}</div>'


def generate_bulletin_page(bulletin: Bulletin) -> str:
    """Generate a bulletin page HTML."""
    content_html = markdown_to_html(bulletin.content)
    metadata_html = generate_metadata_html(bulletin.frontmatter)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bulletin.title} - Bulletin Board</title>
    <style>{get_css()}</style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← Back to all bulletins</a>
        
        <article>
            <h1>{bulletin.title}</h1>
            {metadata_html}
            {content_html}
        </article>
        
        <footer>
            <p>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}</p>
        </footer>
    </div>
    <script>{get_bulletin_page_js()}</script>
</body>
</html>
"""


def main():
    """Main function to generate the static site."""
    # Find the bulletins directory
    script_dir = Path(__file__).parent
    bulletins_dir = script_dir / "bulletins"
    output_dir = script_dir / "_site"
    
    if not bulletins_dir.exists():
        print(f"Error: Bulletins directory not found at {bulletins_dir}")
        return 1
    
    # Clean and create output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    
    # Find all bulletins
    bulletins = find_bulletins(bulletins_dir)
    
    if not bulletins:
        print("No BULLETIN.md files found")
        # Create a placeholder index page
        index_html = generate_index_page([])
        (output_dir / "index.html").write_text(index_html, encoding="utf-8")
        print(f"Created placeholder site at {output_dir}")
        return 0
    
    print(f"Found {len(bulletins)} bulletin(s):")
    for b in bulletins:
        print(f"  - {b.name}: {b.title}")
    
    # Generate index page
    index_html = generate_index_page(bulletins)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
    print(f"Generated: index.html")
    
    # Generate individual bulletin pages
    for bulletin in bulletins:
        page_html = generate_bulletin_page(bulletin)
        page_path = output_dir / f"{bulletin.name}.html"
        page_path.write_text(page_html, encoding="utf-8")
        print(f"Generated: {bulletin.name}.html")
    
    print(f"\nSite generated successfully at {output_dir}")
    return 0


if __name__ == "__main__":
    exit(main())
