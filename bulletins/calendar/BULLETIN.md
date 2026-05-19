---
cost: 0.4849
title: calendar
updated_at: 2026-05-19T09:16:32.139697
---

| ID | Date | Status | Issue | Required Action | Documentation |
|---|---|---|---|---|---|
| 20260519-auth | 2026-05-19 | ❌ Authentication Error | Google Calendar API requires OAuth2 authentication. API keys are not supported for accessing personal calendar events. Error message: "API keys are not supported by this API. Expected OAuth2 access token or other authentication credentials that assert a principal." | **To access your Google Calendar events, you need OAuth2 authentication:**<br><br>**Option 1: Service Account** (Best for automation):<br>• Create service account in [Google Cloud Console](https://console.cloud.google.com/)<br>• Download JSON key file<br>• Share your calendar with the service account email<br>• Provide the JSON key file content as a secret to this agent<br><br>**Option 2: OAuth2 Access Token**:<br>• Use Google OAuth Playground to generate temporary token<br>• Note: Expires in 1 hour without refresh token<br><br>**Option 3: Use Calendar Export**:<br>• Export calendar as .ics file<br>• Share the file URL for agent to parse | [Service Account Setup Guide](https://developers.google.com/identity/protocols/oauth2/service-account) • [Calendar API Documentation](https://developers.google.com/calendar/api/guides/auth) • [OAuth Playground](https://developers.google.com/oauthplayground/) |