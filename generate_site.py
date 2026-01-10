#!/usr/bin/env python3
"""
Generate a static website from BULLETIN.md files.

This script finds all BULLETIN.md files in the bulletins directory,
converts them to nicely styled HTML pages, and generates an index page.
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Bulletin:
    """Represents a bulletin with its metadata and content."""
    name: str
    title: str
    path: Path
    content: str
    last_updated: str | None = None


def find_bulletins(bulletins_dir: Path) -> list[Bulletin]:
    """Find all BULLETIN.md files in the bulletins directory."""
    bulletins = []
    
    for bulletin_file in bulletins_dir.rglob("BULLETIN.md"):
        folder_name = bulletin_file.parent.name
        content = bulletin_file.read_text(encoding="utf-8")
        
        # Extract title from first H1 heading
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else folder_name.replace("-", " ").title()
        
        # Extract last updated date
        last_updated = None
        date_match = re.search(r"\*\*Last Updated:\*\*\s*(.+?)(?:\s*$|\s*\n)", content)
        if date_match:
            last_updated = date_match.group(1).strip()
        
        bulletins.append(Bulletin(
            name=folder_name,
            title=title,
            path=bulletin_file,
            content=content,
            last_updated=last_updated
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
    """Convert markdown table lines to HTML table."""
    if len(lines) < 2:
        return "\n".join(lines)
    
    def parse_row(line: str) -> list[str]:
        # Remove leading/trailing pipes and split
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [cell.strip() for cell in line.split("|")]
    
    # Parse header
    headers = parse_row(lines[0])
    
    # Skip separator line (lines[1])
    
    # Parse body rows
    rows = [parse_row(line) for line in lines[2:] if not re.match(r"^[\s-:|]+$", line)]
    
    # Build HTML table
    html = ['<div class="table-wrapper">', '<table>']
    
    # Header
    html.append("<thead><tr>")
    for header in headers:
        html.append(f"<th>{header}</th>")
    html.append("</tr></thead>")
    
    # Body
    if rows:
        html.append("<tbody>")
        for row in rows:
            html.append("<tr>")
            for i, cell in enumerate(row):
                # Pad with empty cells if row is shorter than header
                html.append(f"<td>{cell}</td>")
            # Add empty cells if row is shorter
            for _ in range(len(headers) - len(row)):
                html.append("<td></td>")
            html.append("</tr>")
        html.append("</tbody>")
    
    html.append("</table>")
    html.append("</div>")
    
    return "\n".join(html)


def get_css() -> str:
    """Return the CSS for the website."""
    return """
:root {
    --bg-color: #1a1b26;
    --card-bg: #24283b;
    --text-color: #a9b1d6;
    --text-muted: #565f89;
    --heading-color: #c0caf5;
    --accent-color: #7aa2f7;
    --accent-hover: #89b4fa;
    --link-color: #7dcfff;
    --border-color: #414868;
    --success-color: #9ece6a;
    --warning-color: #e0af68;
    --table-header-bg: #1f2335;
    --table-row-alt: #292e42;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
    min-height: 100vh;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

header {
    text-align: center;
    padding: 3rem 0;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 2rem;
}

header h1 {
    color: var(--heading-color);
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

header p {
    color: var(--text-muted);
    font-size: 1.1rem;
}

.back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--accent-color);
    text-decoration: none;
    margin-bottom: 2rem;
    font-size: 0.95rem;
    transition: color 0.2s;
}

.back-link:hover {
    color: var(--accent-hover);
}

/* Bulletin list on index page */
.bulletin-list {
    display: grid;
    gap: 1.5rem;
}

.bulletin-card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid var(--border-color);
    transition: transform 0.2s, box-shadow 0.2s;
}

.bulletin-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.bulletin-card h2 {
    color: var(--heading-color);
    margin-bottom: 0.5rem;
}

.bulletin-card h2 a {
    color: inherit;
    text-decoration: none;
}

.bulletin-card h2 a:hover {
    color: var(--accent-color);
}

.bulletin-card .meta {
    color: var(--text-muted);
    font-size: 0.9rem;
}

/* Article content */
article {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 2rem;
    border: 1px solid var(--border-color);
}

article h1 {
    color: var(--heading-color);
    font-size: 2rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
}

article h2 {
    color: var(--heading-color);
    font-size: 1.5rem;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

article h3 {
    color: var(--heading-color);
    font-size: 1.25rem;
    margin: 1.5rem 0 0.75rem;
}

article h4, article h5, article h6 {
    color: var(--heading-color);
    margin: 1rem 0 0.5rem;
}

article p {
    margin: 1rem 0;
}

article a {
    color: var(--link-color);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
}

article a:hover {
    border-bottom-color: var(--link-color);
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
    border-top: 1px solid var(--border-color);
    margin: 2rem 0;
}

article strong {
    color: var(--heading-color);
}

article code {
    background: var(--table-header-bg);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-size: 0.9em;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

article pre {
    background: var(--table-header-bg);
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1rem 0;
}

article pre code {
    background: none;
    padding: 0;
}

/* Tables */
.table-wrapper {
    overflow-x: auto;
    margin: 1.5rem 0;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
}

th {
    background: var(--table-header-bg);
    color: var(--heading-color);
    font-weight: 600;
    text-align: left;
    padding: 0.75rem 1rem;
    border-bottom: 2px solid var(--border-color);
}

td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-color);
}

tr:nth-child(even) {
    background: var(--table-row-alt);
}

tr:last-child td {
    border-bottom: none;
}

/* Footer */
footer {
    text-align: center;
    padding: 2rem 0;
    margin-top: 2rem;
    border-top: 1px solid var(--border-color);
    color: var(--text-muted);
    font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
    
    header h1 {
        font-size: 1.75rem;
    }
    
    article {
        padding: 1.25rem;
    }
    
    article h1 {
        font-size: 1.5rem;
    }
}
"""


def generate_index_page(bulletins: list[Bulletin]) -> str:
    """Generate the index page HTML."""
    bulletin_cards = []
    for b in bulletins:
        meta = f"Last updated: {b.last_updated}" if b.last_updated else ""
        bulletin_cards.append(f"""
        <div class="bulletin-card">
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
</body>
</html>
"""


def generate_bulletin_page(bulletin: Bulletin) -> str:
    """Generate a bulletin page HTML."""
    content_html = markdown_to_html(bulletin.content)
    
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
            {content_html}
        </article>
        
        <footer>
            <p>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}</p>
        </footer>
    </div>
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
