---
cost: 0.6224
title: calendar
updated_at: 2026-05-16T08:39:20.819423
---

| ID | Date | Status | Issue | Required Action | Documentation |
|---|---|---|---|---|---|
| 20260516-auth | 2026-05-16 | ❌ Authentication Error | Google Calendar API requires OAuth2 authentication. API keys are not supported for accessing personal calendar events. Error message: "API keys are not supported by this API. Expected OAuth2 access token or other authentication credentials that assert a principal." | **To access your Google Calendar events, use one of these methods:**<br>**1. Service Account** (Recommended for automation):<br>• Create service account in Google Cloud Console<br>• Enable Domain-Wide Delegation if needed<br>• Share calendar with service account email<br>• Download JSON key file and provide to agent<br>**2. OAuth2 Token** (For personal use):<br>• Create OAuth2 credentials<br>• Generate access token with calendar scope<br>• Note: Tokens expire every 3-4 hours without refresh<br>**3. Third-party Tools**:<br>• Use Cal.com or similar services that handle OAuth<br>• These can sync with Google Calendar | [Service Account Guide](https://medium.com/product-monday/accessing-google-calendar-api-with-service-account-a99aa0f7f743) • [Google API Auth](https://cloud.google.com/docs/authentication) • [Python without OAuth Screen](https://notes.nicolasdeville.com/helpers/google-api-without-consent-screen) |