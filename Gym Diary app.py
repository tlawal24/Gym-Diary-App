import sqlite3
import hashlib

# Initialize database
conn = sqlite3.connect('gym_diary.db')
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    exercise TEXT NOT NULL,
                    sets INTEGER,
                    reps INTEGER,
                    weight REAL,
                    date DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

conn.commit()


class GymDiary:
    def __init__(self):
        self.logged_in_user = None

    def register(self, username, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()

    def login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        if user:
            self.logged_in_user = user[0]
            print("Login successful.")
        else:
            print("Invalid username or password.")


    def add_workout(self, exercise, sets, reps, weight):
        if not self.logged_in_user:
            print("Please login first.")
            return

        cursor.execute("INSERT INTO workouts (user_id, exercise, sets, reps, weight, date) VALUES (?, ?, ?, ?, ?, DATE('now'))",
                       (self.logged_in_user, exercise, sets, reps, weight))
        conn.commit()
        print("Workout added successfully!")

def view_body_measurements(self):
    if not self.logged_in_user:
        print("Please login first.")
        return

    cursor.execute("SELECT * FROM body_measurements WHERE user_id=? ORDER BY date DESC", (self.logged_in_user,))
    measurements = cursor.fetchall()

    if not measurements:
        print("No body measurements found.")
    else:
        print("Body Measurements:")
        for measurement in measurements:
            print(f"Date: {measurement[4]}, Weight: {measurement[2]} kg, Body Fat: {measurement[3]}%,")


    def quit(self):
        conn.close()
        print("Goodbye!")


# Main program loop
gym_diary = GymDiary()

while True:
    print("Gym Diary Menu:")
    print("1. Register")
    print("2. Login")
    print("3. Add Workout")
    print("4. View Workout History")
    print("5. Add Body Measurement")
    print("6. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        gym_diary.register(username, email, password)

    elif choice == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        gym_diary.login(username, password)

    elif choice == '3':
        exercise = input("Enter exercise name: ")
        sets = int(input("Enter number of sets: "))
        reps = int(input("Enter number of reps: "))
        weight = float(input("Enter weight (in kg): "))
        gym_diary.add_workout(exercise, sets, reps, weight)

    elif choice == '4':
        gym_diary.view_workout_history()


    elif choice =='5':
        date = input("Enter the date: ")
        weight = float(input("Enter weight (in kg):"))
        fat = int(input("Enter body fat% :"))
    
        

    elif choice == '6':
        gym_diary.quit()
        break

    else:
        print("Invalid choice. Please try again.")


