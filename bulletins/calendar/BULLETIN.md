---
cost: 0.3958
title: calendar
updated_at: 2026-04-20T08:51:20.584963
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260420-auth | 2026-04-20 | ⚠️ Authentication Required | Google Calendar API requires OAuth2 or Service Account authentication for private calendar access. API keys alone cannot access private calendar events. | **To access your calendar, please provide:** 1) **OAuth2 Token**: Set up OAuth2 and provide refresh token ([Setup Guide](https://developers.google.com/calendar/api/guides/auth)) 2) **Service Account JSON**: Create service account, share calendar with it, provide JSON key ([Service Account Guide](https://developers.google.com/identity/protocols/oauth2/service-account)) 3) **Make Calendar Public**: Share calendar publicly and provide Calendar ID to use with API key |