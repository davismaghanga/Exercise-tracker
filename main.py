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
    print("🏋️ Manual Exercise Tracker (No API)")
    print("Paste structured exercise JSON like below:\n")
    print('[{"exercise": "running", "duration_minutes": 30}]\n')

    while True:
        user_input = input("Paste JSON (or 'q' to quit):\n> ")
        if user_input.strip().lower() in ['q', 'quit', 'exit']:
            break

        try:
            exercises = json.loads(user_input)
        except json.JSONDecodeError:
            print("❌ Invalid JSON. Try again.\n")
            continue

        now = datetime.now()
        for entry in exercises:
            exercise = entry.get("exercise")
            duration_raw = entry.get("duration_minutes", 0)

            try:
                duration = int(float(duration_raw))  # handles "20", "20.0", even 20.5
            except (ValueError, TypeError):
                print(f"⚠️ Invalid duration value: {duration_raw}. Defaulting to 0.")
                duration = 0
            calories = calculate_calories(exercise, duration)

            row = [
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M"),
                exercise,
                f"{duration} minutes",
                calories
            ]

            try:
                SHEET.append_row(row)
                print(f"✅ Logged: {exercise}, {duration} min, {calories} cal")
            except Exception as e:
                print("❌ Error writing to Google Sheets:", str(e))
        print()

if __name__ == "__main__":
    main()
