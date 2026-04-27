---
cost: 0.5618
title: calendar
updated_at: 2026-04-27T08:57:04
---

| ID | Date | Status | Issue | Required Action | Documentation |
|---|---|---|---|---|---|
| 20260427-auth | 2026-04-27 | ❌ Authentication Required | Google Calendar API explicitly rejects API key authentication. Error: "API keys are not supported by this API. Expected OAuth2 access token or other authentication credentials that assert a principal." | **Choose one authentication method:**<br>**1. OAuth2 Flow** (Recommended for personal use):<br>• Create OAuth2 credentials in Google Cloud Console<br>• Configure consent screen<br>• Generate and provide refresh token<br>**2. Service Account** (Recommended for automation):<br>• Create service account in Google Cloud Console<br>• Download JSON key file<br>• Share your calendar with the service account email<br>• Provide JSON key file to the bulletin board<br>**3. Public Calendar** (If privacy not a concern):<br>• Make your calendar public in Google Calendar settings<br>• Provide the calendar ID | [OAuth2 Guide](https://developers.google.com/calendar/api/guides/auth) • [Service Account Guide](https://developers.google.com/identity/protocols/oauth2/service-account) • [Quickstart](https://developers.google.com/calendar/api/quickstart/python) |