import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import plotly.express as px

# --- Page Title and Information ---
st.set_page_config(page_title="Insight Deck Dashboard", layout="wide")
st.title("🎓 Insight Deck Dashboard")
st.markdown("""
This interactive dashboard provides a clear and dynamic view of our student community. 
Use the Control Panel sidebar on the left to filter, search, and manage the data.
""")

# The file uploader is in the sidebar
file = st.sidebar.file_uploader("Upload your data file", type=["xlsx", "csv"])
    
# The rest of the app only runs if a file is uploaded
if file is not None:
    try:
        # Correctly read either Excel or CSV files
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
        search_query = st.sidebar.text_input("Search Students", placeholder="Search by Name or Email...")
        
        unique_branches = sorted(df["Branch"].unique())
        unique_years = sorted(df["Year"].unique())
        all_interests_list = [interest.strip() for interests in df["Interests"].dropna() for interest in interests.split(',') if interest.strip()]
        unique_interests = sorted(list(set(all_interests_list)))

        selected_branches = st.sidebar.multiselect("Filter by Branch", options=unique_branches, default=unique_branches)
        selected_years = st.sidebar.multiselect("Filter by Year", options=unique_years, default=unique_years)
        selected_interests = st.sidebar.multiselect("Filter by Interests", options=unique_interests)

        # --- Filtering Logic ---
        df_filtered = df.copy()
        if search_query:
            df_filtered = df_filtered[
                df_filtered["Name"].str.contains(search_query, case=False, na=False) |
                df_filtered["Email"].str.contains(search_query, case=False, na=False)
            ]
        if selected_branches:
            df_filtered = df_filtered[df_filtered["Branch"].isin(selected_branches)]
        if selected_years:
            df_filtered = df_filtered[df_filtered["Year"].isin(selected_years)]
        if selected_interests:
            df_filtered = df_filtered[df_filtered["Interests"].apply(
                lambda x: any(interest in x for interest in selected_interests)
            )]
            
        st.sidebar.download_button(
            label="Export Filtered Data",
            data=df_filtered.to_csv(index=False).encode('utf-8'),
            file_name='filtered_student_data.csv',
            mime='text/csv'
        )

        # --- Main Content with Tabs ---
        data_tab, analytics_tab = st.tabs(["📋 Data & Email", "📊 Analytics Dashboard"])

        # --- Tab 1: Data Table and Email Composer ---
        with data_tab:
            st.header("Filtered Student Data")
            st.info(f"Showing {len(df_filtered)} of {len(df)} students.")

            df_display = df_filtered.copy()
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
                email_subject = st.text_input("Email Subject")
                email_body_template = st.text_area("Draft your message")

                if st.button("Preview & Generate Emails"):
                    st.subheader("Generated Emails Preview")
                    for _, student in selected_students.iterrows():
                        personalized_body = email_body_template.format(Name=student['Name'])
                        with st.expander(f"To: {student['Name']} ({student['Email']})"):
                            st.write(f"**Subject:** {email_subject}")
                            st.code(personalized_body)
            else:
                st.info("Select one or more students from the table above to compose an email.")

        # --- Tab 2: Analytics Dashboard ---
        with analytics_tab:
            st.header("Analytics Dashboard")
            st.write("Visualizations based on the **filtered data** set in the sidebar.")

            if not df_filtered.empty:
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Students per Branch")
                    branch_counts = df_filtered['Branch'].value_counts()
                    st.bar_chart(branch_counts)

                with col2:
                    st.subheader("Students per Year")
                    year_counts = df_filtered['Year'].value_counts().sort_index()
                    st.bar_chart(year_counts)

                

                # --- Top Interests ---
                st.subheader("Top 10 Interests")
                filtered_interests_list = [
                    interest.strip()
                    for interests in df_filtered["Interests"].dropna()
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


                # --- NEW: Branch vs Year Heatmap ---
                st.subheader("Branch vs. Year Distribution")
                
                # Create a pivot table to get the counts
                heatmap_data = pd.crosstab(df_filtered['Branch'], df_filtered['Year'])
                
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