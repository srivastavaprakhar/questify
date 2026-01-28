import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("trial1.db")
cursor = conn.cursor()

# Create the events table
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    event_date TEXT,
    location TEXT
)
''')

# Create academic_calendar table
cursor.execute('''
CREATE TABLE IF NOT EXISTS academic_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    description TEXT
)
''')

# Define Event class
class Event:
    def __init__(self, title, description, event_date, location):
        self.title = title
        self.description = description
        self.event_date = event_date
        self.location = location

    def save_to_db(self, cursor):
        cursor.execute('''
            INSERT INTO events (title, description, event_date, location)
            VALUES (?, ?, ?, ?)
        ''', (self.title, self.description, self.event_date, self.location))

# Define AcademicEvent class
class AcademicEvent:
    def __init__(self, title, start_date, end_date, description):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

    def save_to_db(self, cursor):
        cursor.execute('''
            INSERT INTO academic_calendar (title, start_date, end_date, description)
            VALUES (?, ?, ?, ?)
        ''', (self.title, self.start_date, self.end_date, self.description))

# Insert academic calendar events
academic_events = [
    AcademicEvent("Opening of the fee payment portal", "2023-06-26", "2023-06-26", "Portal opens for all students to pay academic fees."),
    AcademicEvent("Start of academic registration for higher semesters", "2023-06-29", "2023-06-29", "Academic registration begins for students in higher semesters."),
    AcademicEvent("PhD Entrance Examination", "2023-07-07", "2023-07-07", "Entrance examination for PhD applicants."),
    AcademicEvent("Orientation Program for PhD Scholars", "2023-07-08", "2023-07-08", "Induction and orientation for newly admitted PhD students."),
    AcademicEvent("Last date for fee payment", "2023-07-09", "2023-07-09", "Deadline for academic fee payment for all students."),
    AcademicEvent("Publication of result for PhD admission", "2023-07-10", "2023-07-10", "Results for PhD entrance exam announced."),
    AcademicEvent("Commencement of classes (Higher Semesters)", "2023-07-11", "2023-07-11", "Start of lectures for higher semester students."),
    AcademicEvent("Raksha Bandhan", "2023-08-30", "2023-08-30", "Festival holiday."),
    AcademicEvent("Student Council Election", "2023-09-04", "2023-09-04", "Election for student body representatives."),
    AcademicEvent("Techideate / TEDx", "2023-10-14", "2023-10-15", "Technical fest and TEDx event."),
    AcademicEvent("Diwali", "2023-11-12", "2023-11-12", "Diwali holiday."),
    AcademicEvent("Start of ETEs (Higher Semesters)", "2023-11-25", "2023-11-25", "End term exams begin for higher semester students."),
    AcademicEvent("Start of Winter Break (Higher Semesters)", "2023-12-08", "2023-12-08", "Winter vacation for higher semester students begins."),
    AcademicEvent("Start of academic registration for even semester", "2024-01-05", "2024-01-05", "Registration starts for the even semester."),
    AcademicEvent("Commencement of classes (Even Semester)", "2024-01-08", "2024-01-08", "Classes begin for all students for even semester."),
    AcademicEvent("Onerios (Cultural Fest)", "2024-02-29", "2024-03-02", "Annual cultural festival at MUJ."),
    AcademicEvent("Start of MTEs (All Semesters)", "2024-03-04", "2024-03-08", "Mid Term Examinations for all students."),
    AcademicEvent("Holi", "2024-03-25", "2024-03-25", "Festival of colors."),
    AcademicEvent("Start of ETEs (All Semesters)", "2024-05-03", "2024-05-17", "End Term Exams for all students."),
    AcademicEvent("Start of Summer Break", "2024-05-18", "2024-05-18", "Beginning of summer vacation for all students.")
]

# Insert events
events = [
    Event("#include", "The competition kicked off...", "Feb 22, 2025", "Manipal University Jaipur"),
    Event("ACM ROCS (Research Opportunities in Computer Science)", "The \"ACM ROCS,\"", "Nov 23, 2024", "Manipal University Jaipur"),
    Event("International Symposium for Data Science", "The International...", "Nov 07, 2024 - Nov 08, 2024", "Manipal University Jaipur"),
    Event("Elicit'24", "A 3-day Techno cultural...", "Sep 27, 2024 - Sep 29, 2024", "Manipal University Jaipur"),
    Event("Annual General Meeting", "The AGM (Annual General Meeting)...", "Sep 09, 2024", "Manipal University Jaipur"),
    Event("Research Paper Talk", "A Research Paper talk...", "Jun 14, 2024", "Manipal University Jaipur"),
    Event("Altair Datathon", "Altair Datathon is a data...", "Apr 15, 2024 - Apr 16, 2024", "Manipal University Jaipur"),
    Event("Job Junction", "Job Junction, organized...", "Apr 15, 2024 - Apr 16, 2024", "Manipal University Jaipur"),
    Event("ACM India Chapter Summit", "The event took place in...", "Dec 22, 2023 - Dec 23, 2023", "Manipal University Jaipur"),
    Event("International Symposium for Data Science", "International Symposium...", "Nov 08, 2023 - Nov 09, 2023", "Manipal University Jaipur"),
    Event("ELICIT 23", "A 3-day Techno culture...", "Sep 29, 2023 - Oct 02, 2023", "Manipal University Jaipur")
]

# Save both event types
for e in academic_events:
    e.save_to_db(cursor)
for e in events:
    e.save_to_db(cursor)

# Commit changes and close connection
conn.commit()
conn.close()
