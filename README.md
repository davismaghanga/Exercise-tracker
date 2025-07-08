✅ Step 1: Create a Google Cloud Project
Go to Google Cloud Console
Click "Select a project" → "New Project"
Name it something like: Exercise Tracker

✅ Step 2: Enable Google Sheets API
While inside your project, go to the top search bar and type:
"Google Sheets API"
Click it → Click "Enable"
Repeat this for "Google Drive API" too.

✅ Step 3: Create Service Account
In the sidebar, go to IAM & Admin → Service Accounts
Click "Create Service Account"
Name: exercise-tracker-bot
Click "Create and Continue"
On the next screen, click "Done" (no roles needed)

✅ Step 4: Generate credentials.json
Now that your service account is created, click its name.
Go to the "Keys" tab.
Click "Add Key" → "Create new key"
Choose JSON
It will download a file like: exercise-tracker-bot-123abc.json

👉 Rename it to: credentials.json
👉 Move it into your project folder (same folder as your Python script)

✅ Step 5: Share Your Google Sheet
Open your Google Sheet (Exercise Tracker) Make sure it has 5 columns: (Date	Time	Exercise	Duration	Calories)
Copy the service account email from the JSON file
(it looks like exercise-tracker-bot@your-project.iam.gserviceaccount.com)
In your Google Sheet:
Click "Share"
Paste the email
Give it Editor access
Click Send
