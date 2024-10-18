import datetime

class HealthAndWellnessPlanner:
    def __init__(self):
        self.daily_log = {}

    def log_water_intake(self, day: str, amount: int):
        """Log water intake for a specific day."""
        if day not in self.daily_log:
            self.daily_log[day] = {}
        self.daily_log[day]['Water Intake (ml)'] = self.daily_log[day].get('Water Intake (ml)', 0) + amount

    def log_sleep(self, day: str, hours: float):
        """Log sleep duration for a specific day."""
        if day not in self.daily_log:
            self.daily_log[day] = {}
        self.daily_log[day]['Sleep (hours)'] = hours

    def log_meal(self, day: str, meal_type: str, meal_description: str):
        """Log meals for a specific day (e.g., Breakfast, Lunch, Dinner)."""
        if day not in self.daily_log:
            self.daily_log[day] = {}
        if 'Meals' not in self.daily_log[day]:
            self.daily_log[day]['Meals'] = {}
        self.daily_log[day]['Meals'][meal_type] = meal_description

    def log_wellness_activity(self, day: str, activity: str, duration: int):
        """Log wellness activities like meditation, walking, etc."""
        if day not in self.daily_log:
            self.daily_log[day] = {}
        if 'Wellness Activities' not in self.daily_log[day]:
            self.daily_log[day]['Wellness Activities'] = []
        self.daily_log[day]['Wellness Activities'].append({'Activity': activity, 'Duration (mins)': duration})

    def display_log(self):
        """Display the health and wellness log."""
        for day, log in self.daily_log.items():
            print(f"Health & Wellness Log for {day}:")
            if 'Water Intake (ml)' in log:
                print(f"  Water Intake: {log['Water Intake (ml)']} ml")
            if 'Sleep (hours)' in log:
                print(f"  Sleep: {log['Sleep (hours)']} hours")
            if 'Meals' in log:
                print("  Meals:")
                for meal, description in log['Meals'].items():
                    print(f"    {meal}: {description}")
            if 'Wellness Activities' in log:
                print("  Wellness Activities:")
                for activity in log['Wellness Activities']:
                    print(f"    {activity['Activity']} for {activity['Duration (mins)']} minutes")
            print()

if __name__ == "__main__":
    # Example Usage:
    planner = HealthAndWellnessPlanner()

    # Log activities for Monday
    planner.log_water_intake('Monday', 1500)
    planner.log_sleep('Monday', 8)
    planner.log_meal('Monday', 'Breakfast', 'Oatmeal and fruits')
    planner.log_meal('Monday', 'Lunch', 'Grilled chicken and salad')
    planner.log_wellness_activity('Monday', 'Meditation', 20)
    planner.log_wellness_activity('Monday', 'Walking', 30)

    # Log activities for Tuesday
    planner.log_water_intake('Tuesday', 2000)
    planner.log_sleep('Tuesday', 7)
    planner.log_meal('Tuesday', 'Breakfast', 'Smoothie bowl')
    planner.log_meal('Tuesday', 'Dinner', 'Pasta and vegetables')
    planner.log_wellness_activity('Tuesday', 'Yoga', 45)

    # Display the log
    planner.display_log()
