---
cost: 0.3296
title: calendar
updated_at: 2026-01-15T00:00:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260114-auth | 2026-01-15 | ⚠️ Authentication Required | Cannot access private Google Calendar events. The Google Calendar API requires proper authentication (OAuth 2.0 or Service Account) to access private calendar data, not just an API key. | To view your private calendar meetings, you need one of these authentication methods: **1) OAuth 2.0** - Set up OAuth consent and use user authorization flow, or **2) Service Account** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, share your calendar with the service account email, and provide the full JSON content as credentials. See [Google Calendar API Authentication Guide](https://developers.google.com/calendar/api/guides/auth) for detailed setup instructions. |