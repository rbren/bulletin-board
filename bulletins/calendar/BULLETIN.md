---
cost: 0.5535
title: calendar
updated_at: 2026-04-23T08:41:57.623217
---

| ID | Date | Status | Authentication Issue | Required Action |
|---|---|---|---|---|
| 20260423-auth | 2026-04-23 | ⚠️ Authentication Required | Google Calendar API cannot access private calendars with API key alone. Error: "API keys are not supported by this API. Expected OAuth2 access token or other authentication credentials that assert a principal." | **To access your calendar events, you need to provide one of these:** <br>1) **OAuth2 Credentials**: Create OAuth2 credentials and provide refresh token ([Setup Guide](https://developers.google.com/calendar/api/guides/auth))<br>2) **Service Account**: Create service account, share calendar with it, provide JSON key file ([Service Account Guide](https://developers.google.com/identity/protocols/oauth2/service-account))<br>3) **Make Calendar Public**: Make your calendar public and provide the Calendar ID to use with API key |