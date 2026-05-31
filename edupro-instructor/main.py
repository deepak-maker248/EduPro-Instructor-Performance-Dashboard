import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="EduPro Instructor Performance Dashboard",
    layout="wide"
)

st.title("📊 Instructor Performance and Course Quality Evaluation on EduPro")
st.write("Interactive dashboard for evaluating instructor performance and course quality.")

# Load Data
@st.cache_data
def load_data():
    file = "EduPro Online Platform (2).xlsx"

    users = pd.read_excel(file, sheet_name="Users")
    teachers = pd.read_excel(file, sheet_name="Teachers")
    courses = pd.read_excel(file, sheet_name="Courses")
    transactions = pd.read_excel(file, sheet_name="Transactions")

    return users, teachers, courses, transactions

users, teachers, courses, transactions = load_data()

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dataset Overview",
        "Instructor Leaderboard",
        "Experience vs Rating",
        "Course Quality Analysis",
        "Expertise Insights",
        "KPI Dashboard",
        "Executive Summary"
    ]
)

# DATASET OVERVIEW
if page == "Dataset Overview":

    st.header("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Users", len(users))
    col2.metric("Teachers", len(teachers))
    col3.metric("Courses", len(courses))
    col4.metric("Transactions", len(transactions))

    st.subheader("Teachers Data")
    st.dataframe(teachers.head())

    st.subheader("Courses Data")
    st.dataframe(courses.head())

    st.subheader("Transactions Data")
    st.dataframe(transactions.head())

# INSTRUCTOR LEADERBOARD
elif page == "Instructor Leaderboard":

    st.header("🏆 Instructor Leaderboard")

    top_teachers = teachers.sort_values(
        by="TeacherRating",
        ascending=False
    ).head(10)

    st.dataframe(top_teachers)

    fig = px.bar(
        top_teachers,
        x="TeacherName",
        y="TeacherRating",
        title="Top 10 Instructors"
    )

    st.plotly_chart(fig, use_container_width=True)

# EXPERIENCE VS RATING
elif page == "Experience vs Rating":

    st.header("Experience vs Rating")

    fig = px.scatter(
        teachers,
        x="YearsOfExperience",
        y="TeacherRating",
        color="Expertise",
        hover_name="TeacherName",
        title="Experience vs Rating"
    )

    st.plotly_chart(fig, use_container_width=True)

# COURSE QUALITY ANALYSIS
elif page == "Course Quality Analysis":

    st.header("Course Quality Analysis")

    fig = px.bar(
        courses,
        x="CourseName",
        y="CourseRating",
        color="CourseCategory",
        title="Course Ratings"
    )

    st.plotly_chart(fig, use_container_width=True)

# EXPERTISE INSIGHTS
elif page == "Expertise Insights":

    st.header("Expertise Insights")

    expertise_avg = (
        teachers.groupby("Expertise")["TeacherRating"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        expertise_avg,
        x="Expertise",
        y="TeacherRating",
        title="Average Rating by Expertise"
    )

    st.plotly_chart(fig, use_container_width=True)

# KPI DASHBOARD
elif page == "KPI Dashboard":

    st.header("KPI Dashboard")

    avg_rating = round(teachers["TeacherRating"].mean(), 2)
    avg_exp = round(teachers["YearsOfExperience"].mean(), 2)
    avg_course_rating = round(courses["CourseRating"].mean(), 2)

    c1, c2, c3 = st.columns(3)

    c1.metric("Avg Teacher Rating", avg_rating)
    c2.metric("Avg Experience", avg_exp)
    c3.metric("Avg Course Rating", avg_course_rating)

# EXECUTIVE SUMMARY
elif page == "Executive Summary":

    st.header("Executive Summary")

    st.success(
        """
        Key Findings:

        • Instructor ratings vary significantly across expertise areas.

        • Higher experience generally results in better ratings.

        • Some courses have excellent ratings and should be promoted.

        • Data-driven evaluation helps improve course quality.

        • Top instructors can be identified for recognition and mentoring.
        """
    )