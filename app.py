import streamlit as st
import mysql.connector
import base64

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Smart AI Job Portal", layout="wide")

# ---------------- ULTRA UI BACKGROUND ----------------
def set_bg():
    with open("bg.jpg", "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
        url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
    }}

    h1, h2, h3, h4, p, label {{
        color: white !important;
    }}

    .card {{
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }}

    .stTextInput input {{
        background: rgba(255,255,255,0.9);
        color: black;
        border-radius: 10px;
    }}

    .stButton>button {{
        background: linear-gradient(90deg,#1f77b4,#00c6ff);
        color: white;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg()

# ---------------- DATABASE ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pranjal@3425",
    database="smart_job_portal",
    port=3306
)

cursor = db.cursor()

# ---------------- SESSION ----------------
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;'>💼 Smart AI Job Portal</h1>", unsafe_allow_html=True)

# ---------------- MENU ----------------
menu = [
    "🏠 Register",
    "💼 Recommended Jobs",
    "📍 Search Location",
    "📨 Apply Job",
    "📌 Track Application",
    "🔐 Admin Login",
    "🛠 Admin Panel"
]

choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------
if choice == "🏠 Register":

    st.subheader("📝 Register")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    skill = st.text_input("Skill")

    if st.button("Register"):
        cursor.execute("INSERT INTO users(name,email,password,skill) VALUES(%s,%s,%s,%s)",
                       (name, email, password, skill))
        db.commit()
        st.success("✅ Registered")

# ---------------- JOBS ----------------
elif choice == "💼 Recommended Jobs":

    skill = st.text_input("Enter Skill")

    if st.button("Search"):
        cursor.execute("SELECT * FROM jobs WHERE skill_required LIKE %s",
                       ("%" + skill + "%",))
        jobs = cursor.fetchall()

        for row in jobs:
            st.markdown(f"""
            <div class='card'>
            <h4>{row[1]}</h4>
            <p>📍 {row[3]}</p>
            <p>Status: {row[4]}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------- SEARCH LOCATION ----------------
elif choice == "📍 Search Location":

    location = st.text_input("Enter Location")

    if st.button("Search"):
        cursor.execute("SELECT * FROM jobs WHERE location LIKE %s",
                       ("%" + location + "%",))
        jobs = cursor.fetchall()

        for row in jobs:
            st.markdown(f"""
            <div class='card'>
            <h4>{row[1]}</h4>
            <p>📍 {row[3]}</p>
            <p>Status: {row[4]}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------- APPLY ----------------
elif choice == "📨 Apply Job":

    user_name = st.text_input("Your Name")
    job_title = st.text_input("Job Title")

    if st.button("Apply"):
        cursor.execute(
            "INSERT INTO applications(user_name,job_title,status) VALUES(%s,%s,'Applied')",
            (user_name, job_title)
        )
        db.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        app_id = cursor.fetchone()[0]

        st.success("✅ Applied Successfully")
        st.info(f"📌 Your Application ID: {app_id}")

# ---------------- ADVANCED TRACK ----------------
elif choice == "📌 Track Application":

    st.subheader("📌 Track Your Application")

    option = st.radio("Choose Tracking Method", ["By Application ID", "By Name"])

    # 🔹 Track by ID
    if option == "By Application ID":

        app_id = st.text_input("Enter Application ID")

        if st.button("Track"):

            cursor.execute("SELECT job_title, status FROM applications WHERE id=%s",
                           (app_id,))
            result = cursor.fetchall()

            if result:
                for row in result:
                    st.success(f"Job: {row[0]} | Status: {row[1]}")
            else:
                st.error("No record found")

    # 🔹 Track by Name (Multiple results)
    else:

        name = st.text_input("Enter Your Name")

        if st.button("Track All"):

            cursor.execute("SELECT id, job_title, status FROM applications WHERE user_name=%s",
                           (name,))
            results = cursor.fetchall()

            if results:
                for row in results:
                    st.markdown(f"""
                    <div class='card'>
                    <p><b>ID:</b> {row[0]}</p>
                    <p><b>Job:</b> {row[1]}</p>
                    <p><b>Status:</b> {row[2]}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("No applications found")

# ---------------- ADMIN LOGIN ----------------
elif choice == "🔐 Admin Login":

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "admin123":
            st.session_state.admin_logged = True
            st.success("✅ Logged in")
        else:
            st.error("Wrong login")

# ---------------- ADMIN PANEL ----------------
elif choice == "🛠 Admin Panel":

    if st.session_state.admin_logged:

        st.subheader("🛠 Admin Panel")

        job_title = st.text_input("Job Title")
        skill = st.text_input("Skill Required")
        location = st.text_input("Location")

        if st.button("Post Job"):
            cursor.execute(
                "INSERT INTO jobs(job_title,skill_required,location,status) VALUES(%s,%s,%s,'Open')",
                (job_title, skill, location)
            )
            db.commit()
            st.success("✅ Job Added")

        st.markdown("### Update Status")

        cursor.execute("SELECT * FROM applications")
        for row in cursor.fetchall():
            st.write(row)

        app_id = st.text_input("Application ID")
        status = st.selectbox("Status", ["Applied","Shortlisted","Selected","Rejected"])

        if st.button("Update"):
            cursor.execute("UPDATE applications SET status=%s WHERE id=%s",
                           (status, app_id))
            db.commit()
            st.success("✅ Updated")

    else:
        st.error("Login first")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Smart AI Job Portal - Advanced Version")