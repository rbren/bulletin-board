---
cost: 0.7236
title: calendar
updated_at: 2026-05-15T09:10:27.037363
---

| ID | Date | Status | Issue | Required Action | Documentation |
|---|---|---|---|---|---|
| 20260515-auth | 2026-05-15 | ❌ Authentication Required | Google Calendar API requires OAuth2 authentication and does not support API key authentication. The provided GOOGLE_API_KEY cannot be used to access personal calendar events. | **Choose one authentication method:**<br>**1. OAuth2 Access Token** (Personal use):<br>• Create OAuth2 credentials in Google Cloud Console<br>• Configure consent screen<br>• Generate OAuth2 access/refresh token<br>**2. Service Account** (Best for automation):<br>• Create service account in GCP Console<br>• Download JSON key file<br>• Share calendar with service account email<br>• Provide JSON key file to bulletin board<br>**3. Calendar Automation Tools** (Alternative):<br>• Use tools like WorkOS Pipes or Carly that handle OAuth<br>• These can access calendar without direct OAuth implementation | [OAuth2 Guide](https://developers.google.com/calendar/api/guides/auth) • [Service Account Setup](https://medium.com/product-monday/accessing-google-calendar-api-with-service-account-a99aa0f7f743) • [WorkOS Alternative](https://workos.com/blog/sync-google-calendar-without-oauth) |