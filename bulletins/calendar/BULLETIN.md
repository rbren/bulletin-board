# Calendar Bulletin

**Last Updated:** 2026-01-10

## Status: Configuration Required

This bulletin is designed to display upcoming non-recurring meetings from your Google Calendar, but it requires additional configuration to function properly.

### Missing Configuration

**GOOGLE_API_KEY** - This environment variable is not currently set. To enable this bulletin:

1. **Create a Google Calendar API Key:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create credentials (API key or OAuth 2.0 credentials)
   - Alternatively, use a Service Account for server-to-server access

2. **Add the API Key to GitHub Secrets:**
   - Navigate to your repository settings
   - Go to Secrets and Variables → Actions
   - Add a new secret named `GOOGLE_API_KEY`
   - Update `.github/workflows/update-bulletins.yml` to pass this secret to the calendar bulletin generation

3. **Update the Workflow:**
   Add the following line to the workflow's environment variables section for the calendar bulletin:
   ```yaml
   GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
   ```

### What This Bulletin Will Show

Once configured, this bulletin will automatically display:
- **Non-recurring meetings** scheduled for the next week
- **Participant information** for each meeting
- **External organizations** involved in meetings
- **Meeting details** such as time, location, and description

### Alternative Approaches

If you prefer not to use the Google Calendar API, consider:
- Using Google Calendar's iCal export URL for a simpler integration
- Implementing OAuth 2.0 flow for more secure access
- Using Google Calendar's webhook notifications for real-time updates

---

*This bulletin will be automatically populated with your upcoming meetings once the Google Calendar API access is configured.*
