---
cost: 0.7894
title: calendar
updated_at: 2026-04-07T08:32:09Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260407-auth | 2026-04-07 | ⚠️ Authentication Required | Cannot access Google Calendar events. The Google Calendar API requires OAuth2 authentication for all calendar access (private or public). API keys are not supported. As of 2026-04-07, this remains the case per [Google's API documentation](https://developers.google.com/workspace/calendar/api/guides/auth). | **Option 1: Service Account (Recommended for automation)** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, and share your calendar with the service account email. See [service account documentation](https://developers.google.com/identity/protocols/oauth2/service-account). **Option 2: OAuth Flow** - Implement OAuth2 authentication flow to access calendars. Requires user consent but provides full access. See [Google OAuth2 documentation](https://developers.google.com/identity/protocols/oauth2). **Option 3: Alternative Integration** - Consider using calendar sync services that provide API access or export calendar data to a format accessible with API keys. |