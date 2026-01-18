---
cost: 0.3759
title: calendar
updated_at: 2026-01-18T00:00:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260118-auth | 2026-01-18 | ⚠️ Authentication Required | Cannot access private Google Calendar events. The Google Calendar API requires OAuth 2.0 or Service Account authentication, not just an API key. API response: "API keys are not supported by this API. Expected OAuth2 access token or other authentication credentials." | To view your private calendar meetings, you need one of these authentication methods: **1) OAuth 2.0** - Set up OAuth consent and use user authorization flow, or **2) Service Account** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, share your calendar with the service account email, and provide the full JSON content as credentials. See [Google Calendar API Authentication Guide](https://developers.google.com/calendar/api/guides/auth) for detailed setup instructions. |