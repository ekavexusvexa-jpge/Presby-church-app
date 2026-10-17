import streamlit as st
import sqlite3
from datetime import datetime

# Page Configuration for Mobile
st.set_page_config(
    page_title="Presbyterian Church App",
    page_icon="✝️",
    layout="centered"
)

# Initialize Database
def init_db():
    conn = sqlite3.connect('church.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    c.execute("SELECT COUNT(*) FROM announcements")
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO announcements (title, category, author, content, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            "Welcome to Our Digital Fellowship",
            "Catechism",
            "Church Leadership",
            "Grace and Peace be unto you! Welcome to the official Presbyterian Church mobile portal.",
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
    conn.commit() 

    conn.close()

init_db()

# Church Details
CHURCH_NAME = "El Zion Congregation"
LOCATION_NAME = "Asem-Boys M/A, Kumasi, Ghana"
PHONE_NUMBER = "0242353656"
EMAIL_ADDRESS = "asemasafopcg@gmail.com"
FACEBOOK_LIVE_LINK = "https://www.facebook.com/Asem Asafo Congregation"
ADMIN_PIN = "1843"

# Header Banner
st.markdown(f"""
<div style="background: linear-gradient(135deg, #002B49 0%, #005A9C 100%); color: white; padding: 18px; border-radius: 12px; margin-bottom: 15px;">
    <h2 style="margin: 0; color: #FFD700;">✝️ {CHURCH_NAME}</h2>
    <p style="margin: 5px 0 0 0; font-size: 14px;">📍 <b>Location:</b> {LOCATION_NAME}</p>
    <p style="margin: 3px 0 0 0; font-size: 14px;">📞 <b>Call:</b> {PHONE_NUMBER} | ✉️ <b>Email:</b> {EMAIL_ADDRESS}</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2 = st.tabs(["📱 Member App", "⚙️ Catechist Portal"])

# MEMBER VIEW
with tab1:
    st.markdown("### 📹 Live Service")
    st.link_button("Watch Facebook Live Stream", FACEBOOK_LIVE_LINK, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📢 Daily Announcements")
    
    conn = sqlite3.connect('church.db')
    c = conn.cursor()
    c.execute("SELECT title, category, author, content, date FROM announcements ORDER BY id DESC")
    announcements = c.fetchall()
    conn.close()
    
    for title, category, author, content, date in announcements:
        with st.container():
            st.caption(f"**{category}** • {date}")
            st.subheader(title)
            st.write(content)
            st.caption(f"✍️ Published by: **{author}**")
            st.divider()

# LEADER PORTAL
with tab2:
    st.subheader("🔐 Leadership Portal")
    pin = st.text_input("Enter Leader Security PIN:", type="password")
    
    if pin == ADMIN_PIN:
        st.success("Access Granted")
        with st.form("announcement_form", clear_on_submit=True):
            title = st.text_input("Announcement Title")
            category = st.selectbox("Category", ['Catechism', 'Leadership Notice', 'Youth & Session', 'General Announcement'])
            author = st.text_input("Author/Signed By", value="Catechist")
            content = st.text_area("Message / Details")
            submitted = st.form_submit_button("Publish Announcement")
            
            if submitted:
                if title and content and author:
                    conn = sqlite3.connect('church.db')
                    c = conn.cursor()
                    now = datetime.now().strftime("%Y-%m-%d %H:%M")
                    c.execute("INSERT INTO announcements (title, category, author, content, date) VALUES (?, ?, ?, ?, ?)",
                              (title, category, author, content, now))
                    conn.commit()
                    conn.close()
                    st.success("Announcement published    st.rerun()
                else:
                    st.error("Please fill in all fields.")
    elif pin != "":
        st.error("Incorrect PIN.")
