import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ====================== CONFIG & DATA ======================
st.set_page_config(page_title="SMS - School Management System", layout="wide")

DATA_FILE = "school_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"students": [], "staff": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "data" not in st.session_state:
    st.session_state.data = load_data()
    st.session_state.students = st.session_state.data["students"]
    st.session_state.staff = st.session_state.data["staff"]

students = st.session_state.students
staff = st.session_state.staff

# ====================== CUSTOM CSS FOR EXACT DESIGN ======================
st.markdown("""
<style>
    /* Sidebar */
    .css-1d391kg { padding-top: 2rem; background: linear-gradient(to bottom, #1e3a8a, #3b82f6); }
    .sidebar-logo { text-align: center; color: white; }
    .sidebar-logo h1 { font-size: 3rem; margin: 0; }
    .sidebar-logo p { margin: 5px 0; font-size: 1.8rem; font-weight: bold; }
    .sidebar-logo small { font-size: 1rem; color: #bfdbfe; }

    /* Top buttons */
    .top-buttons { display: flex; justify-content: center; gap: 20px; margin: 30px 0; flex-wrap: wrap; }
    .top-btn { padding: 14px 34px; border: none; border-radius: 50px; color: white; font-weight: bold; font-size: 1.1rem; min-width: 150px; box-shadow: 0 8px 15px rgba(0,0,0,0.2); cursor: pointer; }
    .search-btn { background: #9f7aea; }
    .view-btn { background: #48bb78; }
    .update-btn { background: #ffa726; }
    .delete-btn { background: #ef5350; }

    /* Form card */
    .form-card { background: white; border-radius: 20px; padding: 40px; box-shadow: 0 15px 35px rgba(0,0,0,0.12); max-width: 900px; margin: 0 auto; }
    .section-title { text-align: center; font-size: 2rem; color: #1e40af; font-weight: bold; margin-bottom: 30px; }

    /* Action buttons */
    .action-buttons { text-align: center; margin-top: 40px; }
    .btn-action { padding: 14px 32px; border-radius: 50px; font-size: 1.1rem; margin: 10px; }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h1>🎓</h1>
        <p>SMS</p>
        <small>School Management System</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    page = st.radio("Navigation", 
                    ["Student Registration", "Staff Management", "Result Card"],
                    label_visibility="collapsed")

# ====================== TOP BUTTONS ======================
st.markdown("""
<div class="top-buttons">
    <button class="top-btn search-btn" onclick="document.getElementById('search-tab').click()">Search</button>
    <button class="top-btn view-btn" onclick="document.getElementById('view-tab').click()">View</button>
    <button class="top-btn update-btn" onclick="document.getElementById('view-tab').click()">Update</button>
    <button class="top-btn delete-btn" onclick="document.getElementById('view-tab').click()">Delete</button>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; margin:20px;'><h1 style='color:#1e40af;'>School Management System</h1></div>", unsafe_allow_html=True)
st.markdown("---")

# ====================== MAIN TABS ======================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Student Registration", "Staff Management", "View All Records", "Search Records", "Result Card"])

# ====================== TAB 1: Student Registration ======================
with tab1:
    if page != "Student Registration":
        st.info("👈 Select 'Student Registration' from sidebar to activate this form")
    else:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Student Registration Form</h2>', unsafe_allow_html=True)
        
        with st.form("student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name")
                roll = st.number_input("Roll No", min_value=1, step=1)
                dept = st.text_input("Department")
            with col2:
                phone = st.text_input("Phone Number")
                gender = st.selectbox("Gender", ["Select Gender", "Male", "Female"])
                date = st.date_input("Submission Date", value=datetime.today())
            
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            submitted = col_btn1.form_submit_button("Register", use_container_width=True)
            col_btn2.form_submit_button("Clear Fields", use_container_width=True)
            col_btn3.form_submit_button("Refresh", use_container_width=True)
            if col_btn4.form_submit_button("Exit", use_container_width=True):
                st.warning("Closing app...")
            
            if submitted:
                if gender == "Select Gender":
                    st.error("Please select gender")
                elif any(s.get("Roll No") == roll for s in students):
                    st.error("Roll No already exists!")
                elif name and dept and phone:
                    students.append({
                        "Name": name, "Roll No": int(roll), "Department": dept,
                        "Phone Number": phone, "Gender": gender, "Submission Date": str(date)
                    })
                    save_data({"students": students, "staff": staff})
                    st.success("Student Registered Successfully!")
                    st.rerun()
                else:
                    st.error("Fill all fields")

        st.markdown('</div>', unsafe_allow_html=True)

# ====================== TAB 2: Staff Management ======================
with tab2:
    if page != "Staff Management":
        st.info("👈 Select 'Staff Management' from sidebar")
    else:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title" style="color:#dc3545;">Staff Management Form</h2>', unsafe_allow_html=True)
        
        with st.form("staff_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                s_name = st.text_input("Name")
                s_id = st.number_input("Staff ID", min_value=1, step=1)
                role = st.text_input("Department / Role")
            with col2:
                s_phone = st.text_input("Phone Number")
                s_gender = st.selectbox("Gender", ["Select", "Male", "Female"])
                s_date = st.date_input("Joining Date", value=datetime.today())
            
            submitted = st.form_submit_button("Register Staff")
            if submitted:
                if s_gender == "Select":
                    st.error("Please select gender")
                elif any(m.get("Staff ID") == s_id for m in staff):
                    st.error("Staff ID already exists!")
                elif s_name and role and s_phone:
                    staff.append({
                        "Name": s_name, "Staff ID": int(s_id), "Department / Role": role,
                        "Phone Number": s_phone, "Gender": s_gender, "Joining Date": str(s_date)
                    })
                    save_data({"students": students, "staff": staff})
                    st.success("Staff Registered Successfully!")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ====================== TAB 3: View Records ======================
with tab3:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" style="color:#28a745;">View All Records</h2>', unsafe_allow_html=True)
    
    if students:
        st.subheader("Students")
        df_s = pd.DataFrame(students)
        edited_s = st.data_editor(df_s, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Save Changes (Students)"):
            st.session_state.students = edited_s.to_dict("records")
            save_data({"students": st.session_state.students, "staff": staff})
            st.success("Updated!")
            st.rerun()
    
    if staff:
        st.subheader("Staff")
        df_st = pd.DataFrame(staff)
        edited_st = st.data_editor(df_st, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Save Changes (Staff)"):
            st.session_state.staff = edited_st.to_dict("records")
            save_data({"students": students, "staff": st.session_state.staff})
            st.success("Updated!")
            st.rerun()
    
    if not students and not staff:
        st.info("No records yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== TAB 4: Search ======================
with tab4:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" style="color:#9f7aea;">Search Records</h2>', unsafe_allow_html=True)
    
    query = st.text_input("Search by Name, Roll/ID, Phone, etc.")
    if query:
        q = query.lower()
        results = []
        for s in students:
            if any(q in str(v).lower() for v in s.values()):
                results.append(("Student", s))
        for m in staff:
            if any(q in str(v).lower() for v in m.values()):
                results.append(("Staff", m))
        
        if results:
            for typ, rec in results:
                st.info(f"**{typ}** → {rec}")
        else:
            st.warning("No results found")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== TAB 5: Result Card ======================
with tab5:
    if page != "Result Card":
        st.info("👈 Select 'Result Card' from sidebar")
    else:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title" style="color:#28a745;">Student Result Card</h2>', unsafe_allow_html=True)
        
        roll = st.number_input("Enter Student Roll No", min_value=1, step=1)
        if st.button("View Result"):
            student = next((s for s in students if s["Roll No"] == roll), None)
            if student:
                st.success("Result Found!")
                st.write(f"**Name:** {student['Name']}")
                st.write(f"**Roll No:** {student['Roll No']}")
                st.write(f"**Department:** {student['Department']}")
                st.markdown("### Mock Annual Result 2025")
                st.write("Math: 92 | Physics: 88 | Chemistry: 90 | English: 85 | Urdu: 89")
                st.write("**Grade: A+ (88.8%)** 🎉")
            else:
                st.error("Student not found!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("School Management System • Fully Functional • Share this link with anyone!")
