---
cost: 0.9989
title: calendar
updated_at: 2026-04-02T08:26:40Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260402-auth | 2026-04-02 | ⚠️ Authentication Required | Cannot access private Google Calendar events. The Google Calendar API requires OAuth2 authentication for accessing user calendars. API keys alone are not sufficient for private calendar access. API returns "API keys are not supported by this API" error (401). | **Option 1: Service Account (Best for automation)** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, share your calendar with the service account email. See [this guide](https://medium.com/iceapple-tech-talks/integration-with-google-calendar-api-using-service-account-1471e6e102c8). **Option 2: Make Calendar Public** - If privacy is not a concern, you can [make your calendar public](https://docs.myeventon.com/documentations/make-google-calendar-public-calendar-id/) and access it with just the API key. **Option 3: Export Calendar** - Use Google Calendar's built-in export features (ICS/XML/RSS) for read-only access without authentication. |