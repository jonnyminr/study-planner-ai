import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from data_manager import load_data, add_record

st.set_page_config(page_title="Smart Study Planner", layout="wide")

# ================== 🌌 GLOBAL STYLING ==================
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #0b1220);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #111827);
    border-right: 1px solid #1f2937;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Card effect */
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 15px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 10px;
    padding: 0.5em 1em;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #1d4ed8, #1e40af);
}

/* Inputs */
input, .stNumberInput input, .stDateInput input {
    background-color: #1f2937 !important;
    color: white !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================== 📚 TITLE ==================
st.title("📚 Smart Study Planner")
st.caption("Track your study time, analyze focus, and improve consistency.")

df = load_data()

# ================== 📝 SIDEBAR ==================
st.sidebar.markdown("## 📝 Add Study Record")

subject = st.sidebar.text_input("Subject Name")
date = st.sidebar.date_input("Study Date", datetime.today())
hours = st.sidebar.number_input("Hours Studied", 0.0, 24.0, step=0.5)

if st.sidebar.button("Save Record"):
    if subject.strip():
        df = add_record(date, subject, hours)
        st.sidebar.success("Record saved!")
    else:
        st.sidebar.error("Enter a subject name")

# ================== LAYOUT ==================
left_col, right_col = st.columns([3, 1])

# ================== 📋 LEFT SIDE ==================
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 All Study Records")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Study Graph - Last 7 Days")

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        last_7_days = pd.date_range(end=datetime.today(), periods=7)
        recent_df = df[df["Date"].isin(last_7_days)]

        if not recent_df.empty:
            pivot = recent_df.pivot_table(index="Date", columns="Subject", values="Hours", aggfunc="sum").fillna(0)
            pivot = pivot.reindex(last_7_days, fill_value=0)

            fig, ax = plt.subplots()
            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#0f172a')

            for subject in pivot.columns:
                ax.plot(pivot.index, pivot[subject], marker='o', linewidth=2)

            ax.set_title("Last 7 Days Study Trend", color="white")
            ax.tick_params(colors='white')
            ax.spines[:].set_color('white')
            ax.legend(pivot.columns)

            st.pyplot(fig)
        else:
            st.info("No data for last 7 days")
    else:
        st.info("No records yet")

    st.markdown('</div>', unsafe_allow_html=True)

# ================== 📌 RIGHT SIDE ==================
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📌 Subject Analytics")

    if not df.empty:
        subjects = df["Subject"].unique()
        selected_subject = st.selectbox("Select Subject", subjects)

        subject_total = df[df["Subject"] == selected_subject]["Hours"].sum()
        overall_total = df["Hours"].sum()

        st.markdown(f"### {selected_subject}")
        st.markdown(f"**Total Hours:** {subject_total:.1f}")

        fig2, ax2 = plt.subplots()
        fig2.patch.set_facecolor('#0f172a')
        ax2.set_facecolor('#0f172a')

        ax2.pie(
            [subject_total, overall_total - subject_total],
            labels=[selected_subject, "Other Subjects"],
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'width': 0.4}
        )
        ax2.set_title("Subject Contribution", color="white")

        st.pyplot(fig2)
    else:
        st.info("No data available")

    st.markdown('</div>', unsafe_allow_html=True)
