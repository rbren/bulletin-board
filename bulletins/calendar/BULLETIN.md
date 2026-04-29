---
cost: 0.7310
title: calendar
updated_at: 2026-04-29T08:51:43
---

| ID | Date | Status | Issue | Required Action | Documentation |
|---|---|---|---|---|---|
| 20260429-auth | 2026-04-29 | ❌ Authentication Required | Google Calendar API requires OAuth2 authentication and does not support API key authentication. The provided GOOGLE_API_KEY cannot be used to access personal calendar events. | **Choose one authentication method:**<br>**1. OAuth2 Access Token** (Recommended for personal use):<br>• Create OAuth2 credentials in Google Cloud Console<br>• Configure consent screen<br>• Generate and provide OAuth2 access token or refresh token<br>**2. Service Account** (Recommended for automation):<br>• Create service account in Google Cloud Console<br>• Download JSON key file<br>• Share your calendar with the service account email<br>• Provide JSON key file path to the bulletin board<br>**3. Public Calendar** (If privacy not a concern):<br>• Make your calendar public in Google Calendar settings<br>• Provide the calendar ID for public access | [OAuth2 Guide](https://developers.google.com/calendar/api/guides/auth) • [Service Account Guide](https://developers.google.com/identity/protocols/oauth2/service-account) • [API Reference](https://developers.google.com/calendar/api/v3/reference/events/list) |