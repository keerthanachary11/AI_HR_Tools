import sqlite3

# Connect (or create if it doesn't exist)
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

# Create employees table
cursor.execute('''
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    department TEXT,
    designation TEXT,
    hire_date TEXT,
    salary INTEGER,
    location TEXT
);
''')

# Insert sample data
employees = [
    (1, 'Anita Sharma', 'anita.sharma@example.com', '9876543210', 'HR', 'HR Manager', '2021-06-15', 75000, 'Bengaluru'),
    (2, 'Rohan Mehta', 'rohan.mehta@example.com', '9123456789', 'Tech', 'Software Engineer', '2022-01-10', 90000, 'Remote'),
    (3, 'Priya Desai', 'priya.desai@example.com', '9998776655', 'Marketing', 'Marketing Executive', '2023-03-01', 65000, 'Mumbai'),
    (4, 'Arjun Verma', 'arjun.verma@example.com', '9012345678', 'Tech', 'Senior Developer', '2020-09-20', 110000, 'Bengaluru'),
    (5, 'Neha Kapoor', 'neha.kapoor@example.com', '789012345', 'Finance', 'Accountant', '2021-12-05', 70000, 'Delhi'),
    (6, 'Vikram Rao', 'vikram.rao@example.com', '9112233445', 'Operations', 'Operations Manager', '2019-08-12', 85000, 'Chennai'),
    (7, 'Simran Kaur', 'simran.kaur@example.com', '9777766655', 'HR', 'Recruiter', '2022-11-01', 60000, 'Remote'),
    (8, 'Rahul Nair', 'rahul.nair@example.com', '9090909090', 'Tech', 'DevOps Engineer', '2023-07-10', 95000, 'Bengaluru')
]

cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', employees)

conn.commit()
conn.close()
