---
cost: 0.5595
title: calendar
updated_at: 2026-04-19T08:25:08.970227
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260419-auth | 2026-04-19 | ⚠️ Authentication Required | Cannot access private Google Calendar events with API key alone. The Google Calendar API requires OAuth2 or Service Account authentication for private calendar access. API keys only work for public calendars. | **To enable calendar access, please provide one of the following:** 1) **OAuth2 Credentials**: Set up OAuth2 flow and provide refresh token. See [OAuth2 Guide](https://developers.google.com/workspace/calendar/api/quickstart/python). 2) **Service Account**: Create a service account, share your calendar with the service account email, and provide the JSON key file. See [Service Account Guide](https://developers.google.com/identity/protocols/oauth2/service-account). 3) **Public Calendar ID**: If your calendar is public, provide the calendar ID to access with API key. |