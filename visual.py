import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("User Interaction Evaluation Dashboard")

# Simulated data
methods = ["Button Clicks", "Text Queries"]
interactions = [240, 380]

response_times = [1.3, 1.8]  # in seconds
satisfaction_scores = [4.1, 4.5]  # scale of 5

# Bar chart - Query Method Usage
st.subheader("Interaction Method Usage")
fig1, ax1 = plt.subplots()
ax1.bar(methods, interactions, color=['skyblue', 'salmon'])
ax1.set_ylabel("Number of Interactions")
ax1.set_title("Usage of Button vs. Chat Input")
st.pyplot(fig1)

# Line chart - Response Time
st.subheader("Average Response Time per Method")
fig2, ax2 = plt.subplots()
ax2.plot(methods, response_times, marker='o', linestyle='--', color='green')
ax2.set_ylabel("Response Time (s)")
ax2.set_title("Bot Response Time Comparison")
st.pyplot(fig2)

# Pie chart - User Satisfaction
st.subheader("User Satisfaction by Interaction Type")
fig3, ax3 = plt.subplots()
ax3.pie(satisfaction_scores, labels=methods, autopct='%1.1f%%', startangle=90, colors=['gold', 'lightcoral'])
ax3.set_title("Satisfaction Score Distribution")
st.pyplot(fig3)
