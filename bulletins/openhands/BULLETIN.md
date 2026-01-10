# OpenHands Bulletin Board
*Last Updated: January 10, 2026*

## 🎉 Major News & Announcements

### Series A Funding - $18.8M Raised
**Source:** [OpenHands Blog](https://www.openhands.dev/blog/weve-just-raised-18-8m-to-build-the-open-standard-for-autonomous-software-development) (Posted ~November 19, 2025)

OpenHands raised $18.8M in Series A funding led by Madrona, with participation from:
- Menlo Ventures
- Pillar VC
- Obvious Ventures
- Fujitsu Ventures
- Alumni Ventures

**Key Quote from Soma Somasegar (Madrona):** "OpenHands represents a major shift in how software is built. Autonomous agents are transforming from side-projects into core members of the engineering team, and OpenHands' open, model-agnostic approach ensures this transformation happens safely, transparently, and at enterprise scale."

**Hacker News Discussion:** [4 points, 1 comment](https://news.ycombinator.com/item?id=45975064)

### AMD Partnership Announcement
**Source:** [OpenHands Blog](https://www.openhands.dev/blog/20251119-amd-ryzen-ai-collaboration) (Posted ~November 19, 2025)

Strategic collaboration with AMD to enable local coding agents on Ryzen AI hardware:
- Integration with Lemonade Server for NPU/GPU acceleration
- AMD Ryzen™ AI Max+ 395 processor delivers up to 126 AI TOPS
- Enables running models like Qwen3-Coder-30B locally
- Focus on privacy, cost efficiency, and flexible model selection

**Quote from Adrian Macias (AMD):** "The integration of Lemonade Server with OpenHands reflects AMD's commitment to open-source innovation and developer choice. This collaboration enables local coding agents that prioritize privacy, cost efficiency, and flexible model selection—while taking advantage of acceleration on Ryzen AI PCs."

**Hacker News Discussion:** [2 points, 1 comment](https://news.ycombinator.com/item?id=45994897)

## 📊 Community Metrics

### GitHub Repository Statistics
**Source:** [GitHub API](https://github.com/All-Hands-AI/OpenHands) (As of January 10, 2026)

- ⭐ **66,450 stars** (65K+ reported on website)
- 🍴 **8,230 forks** (7,000+ reported on website)
- 👀 **66,450 watchers**
- 🐛 **190 open issues**
- 📅 **Created:** March 13, 2024
- 🔄 **Last Updated:** January 10, 2026 (active today!)

### Additional Metrics from Official Website
**Source:** [OpenHands.dev](https://www.openhands.dev/)

- 📦 **3+ million downloads**
- 👥 **Hundreds of contributors worldwide**
- 🏢 **Used by engineers at:** AMD, Apple, Google, Amazon, Netflix, TikTok, NVIDIA, Mastercard, VMware

## 🚀 Recent Product Updates

### Version 1.1.0 (December 30, 2025)
**Source:** [GitHub Releases](https://github.com/All-Hands-AI/OpenHands/releases)

**New Features:**
- OAuth 2.0 Device Flow for CLI authentication
- Refresh button in Changes tab
- Export Conversation button for conversation panel
- Forgejo integration support

**Improvements:**
- Changed init process from micromamba to tini for better process management
- Fixed local (non-Docker) runs to use host-writable paths by default
- Multiple UI and performance fixes

**New Contributors:** 8 first-time contributors in this release

### Version 1.0.0 (December 16, 2025)
Major milestone release marking production readiness.

## 📝 Recent Blog Posts & Thought Leadership

### "Agents in the Outer Loop"
**Source:** [OpenHands Blog](https://www.openhands.dev/blog/20251202-agents-in-the-outer-loop) (December 2, 2025)

Discusses the emerging paradigm of cloud-based agents that work in the "outer loop" of development:
- **Inner Loop:** Local IDE/CLI agents that assist developers
- **Outer Loop:** Cloud-based agents invoked from Slack, Jira, GitHub for entire tasks
- Benefits: Enhanced safety (isolated environments) and scalability (parallel execution)
- Research shows 40-50% productivity gains in implementation tasks

**Hacker News Discussion:** [1 point](https://news.ycombinator.com/item?id=46137606)

## 💼 Customer Success Stories

### Real-World Impact
**Source:** [OpenHands Website & Blog](https://www.openhands.dev/)

**Flextract (CTO: Nick Blanchet):**
> "OpenHands autonomously fixes 87% of bug tickets same-day. Our clients think we hired an army of engineers."

**C3.ai (VP of Data Science: Sina Pakazad):**
> "OpenHands was the only solution that let us prompt an autonomous coding agent remotely at scale, not just on a laptop or inside a narrow CI template."

**General Results from Early Adopters:**
- 50% reduction in code maintenance backlogs
- Vulnerability resolution times cut from days to minutes
- Parallel code refactoring across hundreds of repositories

## 🛠️ Product Overview

### Core Offerings

**OpenHands Software Agent SDK**
- Composable Python library for building AI agents
- Run locally or scale to thousands of agents in the cloud
- [Documentation](https://docs.openhands.dev/sdk) | [Source](https://github.com/All-Hands-AI/agent-sdk/)

**OpenHands CLI**
- Command-line interface for easy local usage
- Similar experience to Claude Code or Codex
- Works with Claude, GPT, or any LLM
- [Documentation](https://docs.openhands.dev/openhands/usage/run-openhands/cli-mode) | [Source](https://github.com/OpenHands/OpenHands-CLI)

**OpenHands Local GUI**
- REST API + single-page React application
- Run agents on your laptop
- Similar experience to Devin or Jules
- [Documentation](https://docs.openhands.dev/openhands/usage/run-openhands/local-setup)

**OpenHands Cloud**
- Hosted deployment with $10 free credit
- [Try it here](https://app.all-hands.dev/)
- Features: GitHub/GitLab integrations, Slack/Jira/Linear integrations, multi-user support, RBAC, collaboration features

**OpenHands Enterprise**
- Self-hosted deployment in VPC via Kubernetes
- Source-available with enterprise license
- Includes extended support and research team access
- [Learn more](https://openhands.dev/enterprise)

### Key Differentiators
- ✅ **Open source:** MIT license (except enterprise directory)
- ✅ **Model-agnostic:** Works with any LLM
- ✅ **Secure:** Isolated Docker sandboxes
- ✅ **Scalable:** From one agent to thousands
- ✅ **Integrated:** GitHub, GitLab, Bitbucket, Slack, Jira

## 🔗 Community & Resources

- **GitHub:** https://github.com/OpenHands/OpenHands
- **Documentation:** https://docs.openhands.dev/
- **Website:** https://www.openhands.dev/
- **Slack Community:** https://openhands.dev/joinslack
- **Twitter/X:** https://x.com/OpenHandsDev
- **Blog:** https://www.openhands.dev/blog

## 📈 Common Use Cases

1. **Automated Maintenance Work**
   - Dependency upgrades
   - Fixing merge conflicts
   - Vulnerability sweeps

2. **Large-Scale Refactoring**
   - Coordinated changes across hundreds of repositories
   - Parallel execution

3. **Code Quality Enforcement**
   - Automated PR reviews
   - Adding unit tests
   - Style fixes and best practice enforcement

---

*This bulletin aggregates public information about OpenHands from official sources, GitHub, Hacker News, and other public platforms. All metrics and quotes are attributed to their sources.*
