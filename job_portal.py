import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pranjal@3425",
    database="smart_job_portal"
)

cursor = db.cursor()

while True:

    print("\n===== JOB PORTAL SYSTEM =====")
    print("1. Register")
    print("2. View Jobs")
    print("3. Apply Job")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        name = input("Enter Name: ")
        email = input("Enter Email: ")
        phone = input("Enter Phone: ")
        skills = input("Enter Skills: ")

        sql = "INSERT INTO job_seekers(name,email,phone,skills) VALUES(%s,%s,%s,%s)"
        val = (name,email,phone,skills)

        cursor.execute(sql,val)
        db.commit()

        print("Registration Successful!")

    elif choice == "2":

        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()

        print("\nAvailable Jobs\n")

        for job in jobs:
            print("Job ID:",job[0])
            print("Title:",job[1])
            print("Company:",job[2])
            print("Location:",job[3])
            print("Salary:",job[4])
            print("----------------")

    elif choice == "3":

        user = input("Enter User ID: ")
        job = input("Enter Job ID: ")

        sql = "INSERT INTO applications(user_id,job_id,status) VALUES(%s,%s,'Applied')"
        val = (user,job)

        cursor.execute(sql,val)
        db.commit()

        print("Application Submitted Successfully!")

    elif choice == "4":
        break