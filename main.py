import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import json

# ==== CONFIGURATION ====
DEFAULT_WEIGHT_KG = 70

# MET VALUES
MET_VALUES = {
    "running": 8.3,
    "cycling": 4.0,
    "walking": 3.5,
    "push-ups": 8.0,
    "squats": 5.0,
    "plank": 3.3,
    "jump rope": 12.3,
    "yoga": 2.5,
    "dancing": 5.0
}

# ==== GOOGLE SHEETS SETUP ====
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("Exercise Tracker").sheet1  # Ensure this sheet exists

# ==== CALORIE CALCULATION ====
def calculate_calories(exercise, duration_minutes, weight_kg=DEFAULT_WEIGHT_KG):
    duration_hours = duration_minutes / 60
    met = MET_VALUES.get(exercise.lower(), 4.0)
    calories = round(met * weight_kg * duration_hours, 1)
    return calories

# ==== MAIN WORKFLOW ====
def main():
    print("🏋️ Manual Exercise Tracker")
    print("Enter your exercise type and duration (or type 'q' to quit)\n")

    while True:
        exercise = input("Exercise: ").strip()
        if exercise.lower() in ['q', 'quit', 'exit']:
            break

        duration_input = input("Duration in minutes: ").strip()
        if duration_input.lower() in ['q', 'quit', 'exit']:
            break

        try:
            duration = int(float(duration_input))  # handles '20', '20.0', etc.
        except ValueError:
            print("❌ Invalid duration. Please enter a number.\n")
            continue

        # Compose the structured JSON internally
        exercise_data = {
            "exercise": exercise,
            "duration_minutes": duration
        }

        # Calculate calories
        calories = calculate_calories(exercise_data["exercise"], exercise_data["duration_minutes"])

        # Timestamp
        now = datetime.now()
        row = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M"),
            exercise_data["exercise"],
            f"{exercise_data['duration_minutes']} minutes",
            calories
        ]

        try:
            SHEET.append_row(row)
            print(f"✅ Logged: {exercise}, {duration} min, {calories} cal\n")
        except Exception as e:
            print("❌ Error writing to Google Sheets:", str(e))

if __name__ == "__main__":
    main()