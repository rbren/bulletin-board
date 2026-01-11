---
cost: 0.3341
title: calendar
updated_at: 2026-01-11T18:45:00Z
---

| ID | Date | Status | Issue | Next Steps |
|---|---|---|---|---|
| 20260111-auth | 2026-01-11 | ⚠️ Authentication Issue | Cannot access private Google Calendar events. Current `GOOGLE_API_KEY` is a simple API key (starts with AIzaSy...) which can only access public calendars, not your private meetings. | To view your private calendar meetings, you need: **Service Account** authentication - Create a service account in [Google Cloud Console](https://console.cloud.google.com), download the JSON key file, share your calendar with the service account email, and set `GOOGLE_API_KEY` to the full JSON content. See [Google Calendar API Service Account Setup](https://developers.google.com/calendar/api/guides/auth#service-accounts) for step-by-step instructions. |
