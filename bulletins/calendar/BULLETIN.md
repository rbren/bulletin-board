---
cost: 0.3444
title: calendar
updated_at: 2026-01-13T00:00:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260113-auth | 2026-01-13 | ⚠️ Authentication Required | Cannot access private Google Calendar events. Current `GOOGLE_API_KEY` is a simple API key (starts with AIzaSy...) which can only access public calendars, not your private meetings. | To view your private calendar meetings, you need one of these authentication methods: **1) OAuth 2.0** - Set up OAuth consent and use user authorization flow, or **2) Service Account** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, share your calendar with the service account email, and set `GOOGLE_API_KEY` to the full JSON content. See [Google Calendar API Authentication Guide](https://developers.google.com/calendar/api/guides/auth) for detailed setup instructions. |
