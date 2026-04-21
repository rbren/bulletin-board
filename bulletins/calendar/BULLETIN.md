---
cost: 0.5923
title: calendar
updated_at: 2026-04-21T08:42:56.020553
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260421-auth | 2026-04-21 | ⚠️ Authentication Required | Google Calendar API requires OAuth2 or Service Account authentication for private calendar access. API keys alone cannot access private calendar events. Attempted access returns 404 error. | **To access your calendar, please provide one of the following:** 1) **OAuth2 Credentials**: Set up OAuth2 and provide refresh token ([OAuth2 Setup Guide](https://developers.google.com/calendar/api/guides/auth)) 2) **Service Account JSON**: Create service account, share calendar with it, provide JSON key ([Service Account Guide](https://developers.google.com/identity/protocols/oauth2/service-account)) 3) **Public Calendar**: Make calendar public and provide Calendar ID to use with API key ([Calendar Sharing Guide](https://support.google.com/calendar/answer/37083)) |