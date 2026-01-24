import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("trial1.db")
cursor = conn.cursor()


# Create departments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE NOT NULL
)
''')

# Create faculty table
cursor.execute('''
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    designation TEXT NOT NULL,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
)
''')

# Classes
class Department:
    def __init__(self, name):
        self.name = name

    def save(self, cursor):
        cursor.execute("INSERT OR IGNORE INTO departments (department_name) VALUES (?)", (self.name,))

    def get_id(self, cursor):
        cursor.execute("SELECT department_id FROM departments WHERE department_name = ?", (self.name,))
        return cursor.fetchone()[0]

class Faculty:
    def __init__(self, name, designation, department_id):
        self.name = name
        self.designation = designation
        self.department_id = department_id

    def save(self, cursor):
        cursor.execute('''
            INSERT INTO faculty (name, designation, department_id)
            VALUES (?, ?, ?)
        ''', (self.name, self.designation, self.department_id))
        
departments = [
    ("Department of Economics",),
    ("Department of Journalism and Mass Communication",),
    ("Department of Languages, Literatures and Cultural Studies",),
    ("Department of Arts",)
]

cursor.executemany("INSERT OR IGNORE INTO departments (department_name) VALUES (?)", departments)

# Data from the image
faculty_data = [
    ("Dr. Sunny Dawar", "Associate Professor & HoD (I/C)", "Department of Economics"),
    ("Dr. Garima Singh", "Assistant Professor", "Department of Economics"),
    ("Dr. Minali Banerjee", "Assistant Professor (Senior scale)", "Department of Economics"),
    ("Dr. Monika Mathur", "Associate Professor", "Department of Economics"),
    ("Dr. Namrata Bhardwaj", "Assistant Professor", "Department of Economics"),
    ("Dr. Pushp Kumar", "Assistant Professor", "Department of Economics"),
    ("Dr. Shilpi Gupta", "Associate Professor (Senior Scale)", "Department of Economics"),
    ("Ms. Varuni Sharma", "Assistant Professor (Senior Scale)", "Department of Economics"),
    ("Mr. Vikesh Sharma", "Assistant Professor", "Department of Economics"),
    ("Dr. Trishu Sharma", "Professor & Associate Dean", "Department of Journalism and Mass Communication"),
    ("Dr. Sushil Kumar Rai", "Professor & HoD", "Department of Journalism and Mass Communication"),
    ("Dr. Ajay Soman", "Assistant Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Anuksha Srivastava", "Assistant Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Avneesh Kumar", "Assistant Professor (Senior Scale)", "Department of Journalism and Mass Communication"),
    ("Dr. Fakira Mohan Naik", "Assistant Professor & Director, PR & Media Communication", "Department of Journalism and Mass Communication"),
    ("Dr. Govind Kumar", "Assistant Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Manish Sachan", "Assistant Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Prabhat Dixit", "Assistant Professor (Senior Scale)", "Department of Journalism and Mass Communication"),
    ("Dr. Rachan Daimarry", "Assistant Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Rahul Babu Kodali", "Assistant Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Ram Pratap Singh", "Assistant Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Utsav Krishan Murari", "Assistant Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Vaishali Kapoor", "Associate Professor", "Department of Journalism and Mass Communication"),
    ("Dr. Rabindra Kumar Verma", "Associate Professor (Selection Grade) & HoD (I/C)", "Department of Journalism and Mass Communication"),
    ("Dr. Abinash Mohapatra", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Alka Mathur", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Divya Jyot Kaur", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Eva Sharma", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Gulab Chand", "Assistant Professor (Senior Scale)", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Keshav Nath", "Assistant Professor (Selection Grade)", "Department of Languages, Literatures and Cultural Studies"),
    ("Ms. Navami T. S.", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Neerja Vyas", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Preeti Dahiya", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Priyanka Chaudhary", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Priyanka Yadav", "Assistant Professor (Senior Scale)", "Department of Languages, Literatures and Cultural Studies"),
    ("Ms. Shruti", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Sneha Thakur", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Tanuja Yadav", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Vidisha Gupta", "Assistant Professor", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Yashoda Kumari", "Assistant Professor (Selection Grade)", "Department of Languages, Literatures and Cultural Studies"),
    ("Dr. Richa Arora", "Professor & HoD", "Department of Arts"),
    ("Dr. Atuli Priya", "Assistant Professor (Senior Scale)", "Department of Arts"),
    ("Dr. Anjalee Narayan", "Assistant Professor", "Department of Arts"),
    ("Dr. Anthony Savori Raj", "Assistant Professor", "Department of Arts"),
    ("Dr. Mansi Vani", "Assistant Professor", "Department of Arts"),
    ("Dr. Nagaraj Naragunda", "Assistant Professor", "Department of Arts"),
    ("Dr. Radhika Mohan Gupta", "Assistant Professor", "Department of Arts"),
    ("Dr. Trishna Chaudhuri", "Assistant Professor", "Department of Arts")
]

# Insert departments and faculty
for name, designation, dept in faculty_data:
    department = Department(dept)
    department.save(cursor)
    dept_id = department.get_id(cursor)
    faculty = Faculty(name, designation, dept_id)
    faculty.save(cursor)

# Commit and close
conn.commit()
conn.close()

print("Faculty and departments inserted successfully.")