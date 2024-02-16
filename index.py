import streamlit as st
import matplotlib.pyplot as plt
import sys
import json
import time
import pandas as pd

# Add the path to the directory containing your scraping script
sys.path.append("D:/LEET ANALYZER")

from leetscraper import scrape_leetcode_profile

# Streamlit UI
st.set_page_config(layout='wide')
color1 = '#1f77b4'  # blue
color2 = '#ff7f0e'  # orange

st.title("LeetCode **Profile** Analyzer")
st.write("Compare..Evalute..Improve...")
st.sidebar.header("Enter LeetCode Handles")
#Input for first username
st.sidebar.header("User 1")
profile1 = st.sidebar.text_input("Enter first username:")

# Input for second username
st.sidebar.header("User 2")
profile2 = st.sidebar.text_input("Enter second username:")
# Function to display profile details
def display_profile_details(profile_data, title):
    st.write(f"### {title}")
    st.write("---")
    with st.container():
        st.write(f"**Global Ranking:** {profile_data['global_ranking']}")
        st.write(f"**Contests Attended:** {profile_data['contest_attended']}")
        st.write(f"**Contest Rating:** {profile_data['contest_rating']}")
        st.write(f"**Total Problems Solved:** {profile_data['total_problems_solved']}")
        st.write(f"**Total Problems Submitted:** {profile_data['total_problems']}")
        st.write("#### Problems Solved by Difficulty:")
        st.write(f"- Easy: {profile_data['easy_solved']} / {profile_data['easy_total']}")
        st.write(f"- Medium: {profile_data['medium_solved']} / {profile_data['medium_total']}")
        st.write(f"- Hard: {profile_data['hard_solved']} / {profile_data['hard_total']}")
def draw_circle_meter(problems_solved,total_problems, title):
    fixed_total_problems = 1000  # Set a fixed value for total problems
    fixed_problems_solved = int(problems_solved / total_problems * fixed_total_problems)
    
    fig, ax = plt.subplots(figsize=(5, 5))
    sizes = [fixed_problems_solved, fixed_total_problems - fixed_problems_solved]
    labels = [f"Solved: {problems_solved}", f"Remaining: {total_problems - problems_solved}"]
    colors = ['#1f77b4', '#dddddd']
    ax.pie(sizes, labels=labels, colors=colors, startangle=90, counterclock=False, wedgeprops=dict(width=0.3))
    ax.axis('equal')
    ax.set_title(title, loc='left', fontsize=14, pad=20)
    fig.patch.set_facecolor('#A7E45D')
    st.pyplot(fig)

if st.sidebar.button("Compare"):
    if profile1 and profile2:
        profile_data1 = scrape_leetcode_profile(profile1)
        profile_data2 = scrape_leetcode_profile(profile2)
        
        if profile_data1 and profile_data2:
            col1, col2 = st.columns(2)
            with col1:
                display_profile_details(profile_data1, profile_data1['name'])
                draw_circle_meter(profile_data1['easy_solved'], profile_data1['easy_total'], "Easy Problems")
                draw_circle_meter(profile_data1['medium_solved'], profile_data1['medium_total'], "Medium Problems")
                draw_circle_meter(profile_data1['hard_solved'], profile_data1['hard_total'], "Hard Problems")

            # Display profile details for user 2
            with col2:
                display_profile_details(profile_data2, profile_data2['name'])
                draw_circle_meter(profile_data2['easy_solved'], profile_data2['easy_total'], "Easy Problems")
                draw_circle_meter(profile_data2['medium_solved'], profile_data2['medium_total'], "Medium Problems")
                draw_circle_meter(profile_data2['hard_solved'], profile_data2['hard_total'], "Hard Problems")
        else:
            st.write("Failed to fetch data for one or both usernames.")
    else:
        st.write("Please enter both usernames.")