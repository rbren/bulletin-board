---
cost: 0.3677
title: calendar
updated_at: 2026-01-23T00:00:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260123-auth | 2026-01-23 | ⚠️ Authentication Required | Cannot access private Google Calendar events. The provided GOOGLE_API_KEY is valid but only works for public calendars. Private calendar access requires OAuth 2.0 or Service Account authentication. | To view your private calendar meetings, you need one of these authentication methods: **1) Service Account (Recommended for automation)** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, share your calendar with the service account email, and provide the JSON credentials. **2) OAuth 2.0** - Requires interactive user consent. See [Google Calendar API Authentication Guide](https://developers.google.com/calendar/api/guides/auth) for setup instructions. |