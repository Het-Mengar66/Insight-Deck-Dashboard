# 🎓 Insight Deck: Student Data Dashboard

**Insight Deck** is an interactive web application built with **Streamlit** that allows users to upload, analyze, and interact with student data. It provides powerful filtering capabilities, dynamic data visualizations, and an integrated email composer to engage with specific student groups.



---
## ✨ Core Features

- **📂 Easy Data Upload**: Supports both `.csv` and `.xlsx` file formats for maximum flexibility.
- **🔍 Advanced Filtering**: Dynamically filter the student database by **branch**, **year of study**, and specific **interests**. A text search is also available for names and emails.
- **📊 Analytics Dashboard**: A dedicated tab for data visualization, including:
  - Bar charts for student distribution by branch and year.
  - A Plotly bar chart showcasing the top 10 most common interests.
  - An interactive heatmap showing the intersection of students by branch and year.
- **📋 Interactive Data Table**: View and select students from a clean, sortable table.
- **📩 Integrated Email Composer**: Select students directly from the table to draft and preview personalized emails.
- **📥 Data Export**: Download the filtered dataset as a `.csv` file for offline analysis or record-keeping.

---
## 🛠️ How It Works

The application operates in a few simple steps:
1.  **Upload**: The user uploads a student data file via the sidebar.
2.  **Clean**: The backend script automatically cleans the data, handling missing values to prevent errors.
3.  **Filter**: The user applies filters from the "Control Panel" in the sidebar. The displayed data and analytics update in real-time.
4.  **Visualize**: The "Analytics Dashboard" tab renders various charts and a heatmap based on the filtered data.
5.  **Interact**: In the "Data & Email" tab, the user can select students and use the email composer to draft messages.

---
## 🚀 How to Run Locally

To run this application on your own machine, follow these steps.

### **1. Prerequisites**
- Ensure you have **Python 3.8** or newer installed.

### **2. Clone the Repository**
```bash
git clone [https://github.com/your-username/insight-deck.git](https://github.com/your-username/insight-deck.git)
cd insight-deck
