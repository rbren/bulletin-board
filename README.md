# 📋 Bulletin Board

> Your personal AI-powered news aggregator that keeps you informed about the topics you care about!

## ✨ What is this?

Bulletin Board is an automated system that uses [OpenHands](https://github.com/All-Hands-AI/OpenHands) to search the web and compile curated updates on topics you define. It runs daily, keeping your bulletins fresh and relevant.

Think of it as having a personal research assistant that:
- 🔍 Searches the web for the latest information on your interests
- 📝 Compiles findings into clean, organized markdown tables
- 🗑️ Automatically removes outdated content
- 🌐 Generates a beautiful static website to browse your bulletins

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- An [Anthropic API key](https://console.anthropic.com/) (for Claude)
- A [Tavily API key](https://tavily.com/) (for web search)

### Installation

```bash
# Clone the repository
git clone https://github.com/rbren/bulletin-board.git
cd bulletin-board

# Install dependencies
pip install -r requirements.txt
pip install openhands-sdk openhands-tools
```

### Generate a Bulletin

```bash
# Set your API keys
export LLM_API_KEY=your-anthropic-api-key
export TAVILY_API_KEY=your-tavily-api-key

# Generate a bulletin for a specific topic
python generate_bulletin.py bulletins/concerts/
```

### Generate the Static Site

```bash
python generate_site.py
# Open _site/index.html in your browser
```

## 📁 Project Structure

```
bulletin-board/
├── bulletins/              # Your bulletin topics
│   ├── concerts/           # Example: Local concerts
│   ├── industry-news/      # Example: Tech industry news
│   └── your-topic/         # Add your own!
│       ├── PROMPT.md       # Instructions for the AI
│       └── BULLETIN.md     # Generated bulletin (auto-created)
├── generate_bulletin.py    # AI agent that creates bulletins
├── generate_site.py        # Static site generator
└── PROMPT.md               # Meta-prompt for the AI agent
```

## 🎯 Creating Your Own Bulletin

1. **Create a new folder** in `bulletins/`:
   ```bash
   mkdir bulletins/my-topic
   ```

2. **Add a `PROMPT.md`** file describing what you want to track:
   ```markdown
   Find the latest news about renewable energy technology.
   Focus on solar and wind power innovations.
   Include any major policy changes or company announcements.
   ```

3. **Run the generator**:
   ```bash
   python generate_bulletin.py bulletins/my-topic/
   ```

4. **Check your bulletin** in `bulletins/my-topic/BULLETIN.md`!

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LLM_API_KEY` | Your Anthropic API key | ✅ |
| `TAVILY_API_KEY` | Your Tavily API key for web search | ✅ |
| `GOOGLE_API_KEY` | Google API key (optional) | ❌ |
| `LLM_MODEL` | Model to use (default: `anthropic/claude-opus-4-20250514`) | ❌ |

### Automated Updates with GitHub Actions

This repo includes GitHub Actions workflows that:
- 🔄 **Update bulletins daily** at 8 AM UTC
- 🚀 **Deploy to GitHub Pages** automatically when bulletins change

To enable automated updates in your fork:
1. Add your API keys as repository secrets (`CLAUDE_API_KEY`, `TAVILY_API_KEY`)
2. Enable GitHub Pages in your repository settings
3. That's it! Your bulletins will update automatically

## 📖 Example Bulletins

The repository comes with several example bulletins:

- **🎵 Concerts** - Local music events
- **📰 Industry News** - Tech industry updates
- **🏛️ US Politics** - Political news and updates
- **🤖 OpenHands** - Mentions of OpenHands in the wild
- **📅 Calendar** - Personal calendar events
- **🏘️ Camberville** - Local Cambridge/Somerville news

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new bulletin templates
- Improve the site generator
- Fix bugs or add features
- Share your creative bulletin ideas

## 📄 License

This project is open source. Feel free to use it, modify it, and share it!

---

Made with ❤️ and [OpenHands](https://github.com/All-Hands-AI/OpenHands)
