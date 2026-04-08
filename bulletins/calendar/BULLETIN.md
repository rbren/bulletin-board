---
cost: 0.9010
title: calendar
updated_at: 2026-04-08T08:31:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260408-auth | 2026-04-08 | ⚠️ Authentication Required | Cannot access Google Calendar events with API key. The Google Calendar API requires OAuth2 authentication for all calendar event access, including public calendars. This requirement is confirmed in [Google's April 2026 documentation](https://developers.google.com/workspace/calendar/api/auth). API keys alone cannot retrieve calendar events. | **Option 1: Service Account (Best for automation)** - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, and share your calendar with the service account email. This allows programmatic access without user interaction. See [service account setup guide](https://developers.google.com/identity/protocols/oauth2/service-account). **Option 2: OAuth2 Flow** - Implement OAuth2 authentication to access calendars. Requires initial user consent but provides full access to calendar events. See [OAuth2 implementation guide](https://developers.google.com/workspace/calendar/api/quickstart/python). **Option 3: Calendar Export** - Export calendar data via Google Takeout or use third-party services that bridge Calendar API with simpler authentication methods. |