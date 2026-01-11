---
cost: 0.5221
title: calendar
updated_at: 2026-01-11T12:00:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260111-auth | 2026-01-11 | ⚠️ Authentication Issue | API key authentication cannot access private Google Calendar. Current `GOOGLE_API_KEY` is a simple API key (39 chars) which can only access public calendars. | To access your private calendar events, you need one of: (1) **Service Account** (recommended): Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, and set `GOOGLE_API_KEY` to the entire JSON content, or (2) **OAuth2**: Implement OAuth2 flow for user authentication (more complex for automated scripts). See [Google Calendar API Authentication](https://developers.google.com/calendar/api/guides/auth) for details. |
