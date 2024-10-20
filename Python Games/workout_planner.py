import datetime

class WorkoutPlanner:
    def __init__(self):
        self.workouts = {}
        self.exercises = {
            'Chest': ['Bench Press', 'Push Up', 'Chest Fly'],
            'Back': ['Pull Up', 'Deadlift', 'Bent Over Row'],
            'Legs': ['Squat', 'Lunges', 'Leg Press'],
            'Arms': ['Bicep Curl', 'Tricep Extension', 'Hammer Curl'],
            'Shoulders': ['Overhead Press', 'Lateral Raise', 'Front Raise'],
            'Abs': ['Plank', 'Sit Ups', 'Leg Raises']
        }

    def plan_workout(self, day: str, muscle_group: str, exercises: list):
        """Plan workout for a specific day."""
        if day not in self.workouts:
            self.workouts[day] = []
        self.workouts[day].append({muscle_group: exercises})

    def display_plan(self):
        """Display the workout plan."""
        for day, workout in self.workouts.items():
            print(f"Workout for {day}:")
            for session in workout:
                for muscle_group, exercises in session.items():
                    print(f"  {muscle_group}: {', '.join(exercises)}")
            print()

    def get_available_exercises(self, muscle_group: str):
        """Get available exercises for a muscle group."""
        return self.exercises.get(muscle_group, [])


if __name__ == "__main__":
    # Example Usage:
    planner = WorkoutPlanner()

    # Plan workout for Monday
    planner.plan_workout('Monday', 'Chest', ['Bench Press', 'Push Up'])
    planner.plan_workout('Monday', 'Legs', ['Squat', 'Lunges'])

    # Plan workout for Wednesday
    planner.plan_workout('Wednesday', 'Back', ['Deadlift', 'Pull Up'])
    planner.plan_workout('Wednesday', 'Abs', ['Plank', 'Sit Ups'])

    # Display the workout plan
    planner.display_plan()
