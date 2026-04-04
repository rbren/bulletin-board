---
cost: 0.5655
title: calendar
updated_at: 2026-04-04T08:17:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260403-auth | 2026-04-04 | ⚠️ Authentication Required | Cannot access Google Calendar events. The Google Calendar API no longer supports API key authentication for any calendar access (private or public). OAuth2 authentication is required. Latest test shows 401 UNAUTHENTICATED errors with message: "API keys are not supported by this API. Expected OAuth2 access token or other authentication credentials that assert a principal." | **Option 1: Service Account (Recommended for automation)** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, and share your calendar with the service account email. See [detailed setup guide](https://medium.com/iceapple-tech-talks/integration-with-google-calendar-api-using-service-account-1471e6e102c8). **Option 2: OAuth Flow** - Implement OAuth2 authentication flow to access calendars. Requires user consent but provides full access. See [Google Calendar API quickstart](https://developers.google.com/calendar/api/quickstart/python). **Option 3: Alternative Integration** - Consider using calendar sync services that provide API access or export calendar data to a format accessible with API keys. |