---
cost: 0.4203
title: calendar
updated_at: 2026-04-17T08:39:51.118586
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260417-auth | 2026-04-17 | ⚠️ Authentication Required | Cannot access private Google Calendar events with API key alone. The Google Calendar API requires OAuth2 or Service Account authentication for private calendar access. API keys only work for public calendars. | **Option 1: Service Account with Domain-Wide Delegation** - Best for automated access. Create a service account in [Google Cloud Console](https://console.cloud.google.com), enable domain-wide delegation if needed, and share your calendar with the service account email. [OAuth 2.0 for Server to Server Applications guide](https://developers.google.com/identity/protocols/oauth2/service-account). **Option 2: OAuth2 Flow** - For user-facing applications. Requires initial user consent but provides full calendar access. See [OAuth2 implementation guide](https://developers.google.com/workspace/calendar/api/quickstart/python). **Option 3: Make Calendar Public** - If privacy isn't a concern, make your calendar public and use the API key. Note: All event details will be publicly visible. |