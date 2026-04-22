---
cost: 0.4962
title: calendar
updated_at: 2026-04-22T08:41:05.595351
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260422-auth | 2026-04-22 | ⚠️ Authentication Required | Google Calendar API requires OAuth2 or Service Account authentication for private calendar access. API keys alone cannot access private calendar events. The calendarList endpoint explicitly requires OAuth2, not API key. | **To access your calendar, please provide one of the following:** 1) **OAuth2 Credentials**: Set up OAuth2 and provide refresh token ([OAuth2 Setup Guide](https://developers.google.com/calendar/api/guides/auth)) 2) **Service Account JSON**: Create service account, share calendar with it, provide JSON key ([Service Account Guide](https://developers.google.com/identity/protocols/oauth2/service-account)) 3) **Public Calendar ID**: If you have a public calendar, provide the specific Calendar ID (looks like `example@group.calendar.google.com`) to use with the API key |