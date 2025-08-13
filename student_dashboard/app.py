import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import plotly.express as px
import google.generativeai as genai

# --- Page Title and Information ---
st.set_page_config(page_title="Insight Deck Dashboard", layout="wide")
st.title("🎓 Insight Deck Dashboard")
st.markdown("""
This interactive dashboard provides a clear and dynamic view of our student community. 
Use the Control Panel sidebar on the left to filter, search, and manage the data.
""")

# --- API Key and Model Configuration ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.warning("⚠️ Gemini API Key not found. AI features are disabled.")
    model = None 

file = st.file_uploader("Upload your data file", type=[".xlsx", ".csv"])
    
if file is not None:
    try:
        if file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)


        # --- Data Cleaning ---
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
        df['Branch'] = df['Branch'].fillna('Not Specified')
        df['Interests'] = df['Interests'].fillna('None')
        df['Name'] = df['Name'].fillna('Unknown')
        df['Email'] = df['Email'].fillna('Unknown')

        # --- Sidebar: Control Panel ---
        st.sidebar.header("Control Panel")
        search = st.sidebar.text_input("Search Students", placeholder="Search by Name or Email...")
        
        unique_branches = sorted(df["Branch"].unique())
        unique_years = sorted(df["Year"].unique())
        all_interests_list = [interest.strip() for interests in 
                              df["Interests"].dropna() for interest in interests.split(',') 
                              if interest.strip()
                            ]
        unique_interests = sorted(df["Interests"].unique())


        selected_branches = st.sidebar.multiselect("Filter by Branch", options=unique_branches)
        selected_years = st.sidebar.multiselect("Filter by Year", options=unique_years)
        selected_interests = st.sidebar.multiselect("Filter by Interests", options=unique_interests)

        # --- Filtering Logic ---
        filtered_data = df.copy()
        if search:
            filtered_data = filtered_data[
                filtered_data["Name"].str.contains(search, case=False, na=False) |
                filtered_data["Email"].str.contains(search, case=False, na=False)
            ]
        if selected_branches:
            filtered_data = filtered_data[filtered_data["Branch"].isin(selected_branches)]
        if selected_years:
            filtered_data = filtered_data[filtered_data["Year"].isin(selected_years)]
        if selected_interests:
            filtered_data = filtered_data[filtered_data["Interests"].apply(
                lambda x: any(interest in x for interest in selected_interests)
            )]
            
        st.sidebar.download_button(
            label="⬇️Export Filtered Data",
            data=filtered_data.to_csv(index=False).encode('utf-8'),
            file_name='filtered_student_data.csv',
            mime='text/csv'
        )

        # --- Tabs ---
        data_tab, analytics_tab = st.tabs(["📋 Data & Email", "📊 Analytics Dashboard"])

        # --- Tab 1: Data Table and Email Composer ---
        with data_tab:
            st.header("Filtered Student Data")
            st.info(f"Showing {len(filtered_data)} of {len(df)} students.")

            df_display = filtered_data.copy()
            df_display.insert(0, "Select", False)
            edited_df = st.data_editor(
                df_display,
                hide_index=True,
                column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                disabled=df.columns,
                use_container_width=True
            )
            selected_students = edited_df[edited_df["Select"]]

            st.header("📩 Email Composer")

            if not selected_students.empty:

                st.write(f"You have selected {len(selected_students)} student(s).")
                email_topic = st.text_input("Email Topic", placeholder="e.g., An upcoming Python workshop")
                if st.button("✍️ Generate with AI", use_container_width=True) and model:
                    if email_topic:
                        with st.spinner("Drafting..."):
                            prompt = f"Write a friendly, professional email about: '{email_topic}'. Include '{{Name}}' for personalization and sign off as 'The Coordination Team'."
                            response = model.generate_content(prompt) #Sends the prompt to your AI model.
                            st.session_state.ai_email_draft = response.text
                            #Stores the generated email draft in Streamlit’s session state so it can persist between reruns.
                    else:
                        st.warning("Please enter a topic.")


                email_subject = st.text_input("Email Subject")
                email_body = st.text_area("Email Body", st.session_state.get('ai_email_draft', "Hi {Name},\n"), height=250)

                if st.button("Preview & Generate Emails"):
                    st.subheader("Generated Emails Preview")
                    for _, student in selected_students.iterrows():
                        personalized_body = email_body.format(Name=student['Name'])
                        with st.expander(f"To: {student['Name']} ({student['Email']})"):
                            st.write(f"**Subject:** {email_subject}")
                            st.code(personalized_body)
            else:
                st.info("Select one or more students from the table above to compose an email.")

        # --- Tab 2: Analytics Dashboard ---
        with analytics_tab:
            st.header("Visual Analytics")
            st.write("Visualizations are dynamically updated based on the **filtered data**.")

            if not filtered_data.empty:
                col1, col2 = st.columns(2)

                # Chart 1: Students per Branch
                with col1:
                    st.subheader("Students per Branch")
                    branch_counts = filtered_data['Branch'].value_counts().reset_index()
                    branch_counts.columns = ['Branch', 'Count']
                    fig_branch = px.bar(
                        branch_counts, x='Branch', y='Count',
                        title="Distribution of Students Across Branches",
                        color='Branch', text_auto=True
                    )
                    st.plotly_chart(fig_branch, use_container_width=True)

                # Chart 2: Students per Year
                with col2:
                    st.subheader("Students per Year")
                    year_counts = filtered_data['Year'].value_counts().sort_index().reset_index()
                    year_counts.columns = ['Year', 'Count']
                    fig_year = px.pie(
                        year_counts, names='Year', values='Count',
                        title="Proportion of Students by Year",
                        hole=0.3
                    )
                    st.plotly_chart(fig_year, use_container_width=True)

                # --- Top Interests ---
                st.subheader("Top 10 Interests")
                filtered_interests_list = [
                    interest.strip()
                    for interests in filtered_data["Interests"].dropna()
                    for interest in interests.split(',')
                    if interest.strip()
                ]
                interest_counts = Counter(filtered_interests_list)
                top_interests_df = pd.DataFrame(interest_counts.most_common(10), columns=['Interest', 'Count'])

                fig_interests = px.bar(
                    top_interests_df,
                    x='Interest',
                    y='Count',
                    title='Most Common Interests',
                    text='Count',
                    color='Count',
                )
                fig_interests.update_layout(xaxis_title="Interest", yaxis_title="Number of Students")
                st.plotly_chart(fig_interests, use_container_width=True)


                # --- Branch vs Year Heatmap ---
                st.subheader("Branch v/s Year (Heatmap)")
                
                # Create a pivot table to get the counts
                heatmap_data = pd.crosstab(filtered_data['Branch'], filtered_data['Year'])
                
                # Create the heatmap figure using Plotly Express
                fig = px.imshow(
                    heatmap_data,
                    text_auto=True, # Display the numbers on the heatmap
                    aspect="auto",
                    labels=dict(x="Year of Study", y="Branch", color="Number of Students"),
                    color_continuous_scale=px.colors.sequential.Cividis_r
                )
                fig.update_xaxes(side="top")
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("No data available to display analytics.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a file using the control panel on the left to get started.") 
