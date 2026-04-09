---
cost: 0.8754
title: calendar
updated_at: 2026-04-09T08:38:35.745157+00:00
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260409-auth | 2026-04-09 | ⚠️ Authentication Required | Cannot access private Google Calendar events with API key alone. The Google Calendar API continues to require OAuth2 authentication or Service Account authentication for all private calendar event access. API keys can only access public calendars. Recent [Google Workspace Updates from March 2026](https://workspaceupdates.googleblog.com/2026/03/an-update-on-secondary-calendar-lifecycle-changes-and-a-new-API.html) confirm no changes to authentication requirements. | **Option 1: Service Account with Domain-Wide Delegation** - Best for automated access without user interaction. Create a service account in [Google Cloud Console](https://console.cloud.google.com), enable domain-wide delegation, and share your calendar with the service account. Recent guide from [March 27, 2026](https://notes.nicolasdeville.com/helpers/google-api-without-consent-screen) shows working implementation. **Option 2: OAuth2 Flow** - Implement OAuth2 authentication for full calendar access. Requires initial user consent but provides complete access to calendar events. See [OAuth2 implementation guide](https://developers.google.com/workspace/calendar/api/quickstart/python). **Option 3: Alternative Calendar Export** - Use Google Takeout or third-party services that provide calendar data in accessible formats. |