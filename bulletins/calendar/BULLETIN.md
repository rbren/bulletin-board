---
cost: 0.0000
title: calendar
updated_at: 2026-01-11T00:00:00Z
---

| ID | Status | Issue | Next Steps |
|---|---|---|---|
| 20260111-config | ⚠️ Configuration Required | Google Calendar API credentials not found. The `GOOGLE_API_KEY` environment variable is not set. | Set up Google Calendar API: (1) Create a Google Cloud project at [console.cloud.google.com](https://console.cloud.google.com), (2) Enable the Google Calendar API, (3) Create credentials (API key or OAuth 2.0), (4) Add `GOOGLE_API_KEY` as a GitHub repository secret, (5) Update `.github/workflows/update-bulletins.yml` to pass the key to the calendar bulletin generator. |
