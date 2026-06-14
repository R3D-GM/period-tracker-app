import streamlit as st
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(page_title="Period Tracker", page_icon="🌸", layout="wide")

# Initialize session state for storing data
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'cycle_length' not in st.session_state:
    st.session_state.cycle_length = 28
if 'period_duration' not in st.session_state:
    st.session_state.period_duration = 5

# Title
st.title("🌸 Period & Cycle Tracker")
st.markdown("---")

# Sidebar navigation
menu = st.sidebar.radio("Menu", ["Dashboard", "Log Today", "Calendar", "Insights", "Settings"])

# Function to calculate cycle phase
def get_cycle_phase(day):
    if day <= st.session_state.period_duration:
        return "Menstrual Phase 🩸"
    elif day <= 14:
        return "Follicular Phase 🌱"
    elif day <= 16:
        return "Ovulation Phase 🥚 (Fertile!)"
    else:
        return "Luteal Phase 🌙"

# Dashboard
if menu == "Dashboard":
    st.header("📊 Your Dashboard")
    
    # Get today's cycle day (demo)
    cycle_day = random.randint(1, st.session_state.cycle_length)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Cycle Day", cycle_day, delta=get_cycle_phase(cycle_day))
    with col2:
        next_period = "Soon" if cycle_day > st.session_state.cycle_length - 5 else f"{st.session_state.cycle_length - cycle_day} days"
        st.metric("Next Period", next_period)
    with col3:
        st.metric("Cycle Length", f"{st.session_state.cycle_length} days")
    with col4:
        st.metric("Period Duration", f"{st.session_state.period_duration} days")
    
    st.markdown("---")
    
    # Today's quick log
    st.subheader("📝 Quick Log")
    
    col1, col2 = st.columns(2)
    with col1:
        mood = st.selectbox("How are you feeling?", ["😊 Happy", "😌 Calm", "😢 Sad", "😰 Anxious", "😠 Irritable", "😫 Tired"])
    with col2:
        symptoms = st.multiselect("Symptoms", ["Cramps", "Headache", "Bloating", "Acne", "Fatigue", "Breast Tenderness"])
    
    if st.button("Save Today's Log"):
        st.session_state.logs.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "mood": mood,
            "symptoms": symptoms,
            "cycle_day": cycle_day
        })
        st.success("✅ Log saved successfully!")
        st.balloons()
    
    # Recent logs
    if st.session_state.logs:
        st.subheader("📋 Recent Logs")
        for log in reversed(st.session_state.logs[-5:]):
            st.info(f"**{log['date']}** - {log['mood']} - Symptoms: {', '.join(log['symptoms']) if log['symptoms'] else 'None'}")

# Log Today
elif menu == "Log Today":
    st.header("📝 Detailed Log")
    
    with st.form("log_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            log_date = st.date_input("Date", datetime.now())
            period_flow = st.select_slider("Period Flow", options=["None", "Light", "Medium", "Heavy"], value="None")
        
        with col2:
            mood = st.select_slider("Mood", options=["Very Low", "Low", "Neutral", "Good", "Excellent"])
            energy = st.slider("Energy Level", 0, 100, 50)
        
        st.subheader("🤕 Symptoms")
        symptoms = st.multiselect("Select symptoms", 
            ["Cramps", "Headache", "Bloating", "Acne", "Backache", "Nausea", "Breast Tenderness", "Fatigue"])
        
        st.subheader("📝 Notes")
        notes = st.text_area("Add any notes...")
        
        submitted = st.form_submit_button("Save Log", type="primary")
        
        if submitted:
            st.session_state.logs.append({
                "date": log_date.strftime("%Y-%m-%d"),
                "period_flow": period_flow,
                "mood": mood,
                "energy": energy,
                "symptoms": symptoms,
                "notes": notes
            })
            st.success("✅ Log saved successfully!")
            st.balloons()

# Calendar
elif menu == "Calendar":
    st.header("📅 Calendar View")
    
    # Simple calendar view
    today = datetime.now()
    
    # Create a simple grid
    st.subheader(f"{today.strftime('%B %Y')}")
    
    # Days of week
    cols = st.columns(7)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        cols[i].markdown(f"**{day}**")
    
    # Calendar grid (simplified)
    first_day = today.replace(day=1)
    start_weekday = first_day.weekday()
    
    # Get days in month
    if today.month == 12:
        next_month = today.replace(year=today.year+1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month+1, day=1)
    days_in_month = (next_month - first_day).days
    
    # Display calendar
    current_day = 1
    for week in range(6):
        cols = st.columns(7)
        for day in range(7):
            if week == 0 and day < start_weekday:
                cols[day].write("")
            elif current_day <= days_in_month:
                with cols[day]:
                    st.write(f"**{current_day}**")
                    # Mark predicted period days (demo)
                    if current_day <= st.session_state.period_duration:
                        st.markdown("🩸")
                    elif 14 <= current_day <= 16:
                        st.markdown("🥚")
                current_day += 1
    
    st.info("💡 **Legend:** 🩸 = Period | 🥚 = Fertile Window")

# Insights
elif menu == "Insights":
    st.header("📈 Cycle Insights")
    
    if not st.session_state.logs:
        st.info("📊 Start logging your cycle to see insights and patterns!")
    else:
        # Calculate some basic stats
        total_logs = len(st.session_state.logs)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Logs", total_logs)
        with col2:
            # Count period logs
            period_logs = sum(1 for log in st.session_state.logs if log.get('period_flow', 'None') != 'None')
            st.metric("Period Days Logged", period_logs)
        with col3:
            st.metric("Tracked Cycles", max(1, total_logs // 7))
        
        # Common symptoms
        st.subheader("🔍 Common Symptoms")
        all_symptoms = []
        for log in st.session_state.logs:
            if log.get('symptoms'):
                all_symptoms.extend(log['symptoms'])
        
        if all_symptoms:
            from collections import Counter
            symptom_counts = Counter(all_symptoms)
            for symptom, count in symptom_counts.most_common(5):
                st.progress(count / max(symptom_counts.values()), text=f"{symptom}: {count} times")
        else:
            st.write("No symptoms logged yet")

# Settings
elif menu == "Settings":
    st.header("⚙️ Settings")
    
    st.subheader("Cycle Settings")
    cycle_length = st.slider("Average Cycle Length (days)", 21, 35, st.session_state.cycle_length)
    period_duration = st.slider("Average Period Duration (days)", 2, 10, st.session_state.period_duration)
    
    if cycle_length != st.session_state.cycle_length:
        st.session_state.cycle_length = cycle_length
        st.success("✅ Cycle length updated!")
    
    if period_duration != st.session_state.period_duration:
        st.session_state.period_duration = period_duration
        st.success("✅ Period duration updated!")
    
    st.subheader("🔔 Notifications")
    notifications = st.checkbox("Enable reminders", value=True)
    if notifications:
        st.info("You'll receive period and fertile window reminders")
    
    st.subheader("💾 Data Management")
    if st.button("Export My Data"):
        st.json(st.session_state.logs)
        st.download_button("Download as JSON", str(st.session_state.logs), "period_data.json")
    
    if st.button("Clear All Data", type="secondary"):
        st.session_state.logs = []
        st.warning("All data has been cleared!")

# Footer
st.markdown("---")
st.markdown("🌸 **Your Personal Period Tracker** | Track, Understand, and Thrive")ve")