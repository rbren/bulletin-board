---
cost: 0.6227
title: calendar
updated_at: 2026-04-03T08:22:59Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260403-auth | 2026-04-03 | ⚠️ Authentication Required | Cannot access private Google Calendar events. The Google Calendar API requires OAuth2 authentication for accessing private user calendars. API keys alone are not sufficient. Attempted access returns 404 error when trying to use 'primary' calendar ID without proper OAuth credentials. | **Option 1: Service Account (Recommended for automation)** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, and share your calendar with the service account email. See [detailed setup guide](https://medium.com/iceapple-tech-talks/integration-with-google-calendar-api-using-service-account-1471e6e102c8). **Option 2: Make Calendar Public** - If privacy is not a concern, [make your calendar public](https://support.google.com/calendar/answer/37083) and provide the calendar ID (not 'primary') in the configuration. **Option 3: OAuth Flow** - Implement OAuth2 authentication flow to access private calendars. Requires user consent but provides full access. See [Google Calendar API quickstart](https://developers.google.com/calendar/api/quickstart/python). |