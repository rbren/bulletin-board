---
cost: 0.3870
title: calendar
updated_at: 2026-01-31T00:00:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260131-auth | 2026-01-31 | ⚠️ Authentication Required | Cannot access private Google Calendar events. The Google Calendar API requires OAuth2 authentication for accessing user calendars. API keys alone are not sufficient for private calendar access. Confirmed via API test: "API keys are not supported by this API. Expected OAuth2 access token or other authentication credentials." | To view your private calendar meetings, you need proper authentication: **1) Service Account (Recommended for automation)** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, share your calendar with the service account email, and provide the JSON credentials. **2) OAuth 2.0** - Requires interactive user consent. See [Google Calendar API Authentication Guide](https://developers.google.com/calendar/api/guides/auth) for setup instructions. |