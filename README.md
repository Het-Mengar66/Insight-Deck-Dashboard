# 🎓 Insight Deck: Student Data Dashboard

**Insight Deck** is a sleek, interactive web application powered by **Streamlit** that lets you effortlessly upload, explore, and engage with student data. Designed for educators and administrators, it combines intuitive filtering, rich visual analytics, and seamless communication tools—all in one place.

---

## ✨ Core Features

* **📂 Easy Data Upload**
  Upload your student database in `.csv` or `.xlsx` formats—no hassle, no fuss.

* **🔍 Dynamic Filtering & Search**
  Quickly filter students by **branch**, **year of study**, and **interests**. Plus, a lightning-fast text search for names and emails.

* **📊 Interactive Analytics Dashboard**
  Visualize your data with compelling charts, including:

  * Student counts by branch and year via bar charts.
  * A vibrant Plotly bar chart highlighting the **Top 10 most common interests**.
  * An insightful heatmap showing student distribution across branch-year combinations.

* **📋 Responsive Data Table**
  Explore the filtered data in a sortable, selectable table that adapts to your needs.

* **📩 Built-in Email Composer**
  Select students from the table and draft personalized emails with live previews, making outreach a breeze.

* **📥 Flexible Data Export**
  Export your filtered dataset anytime as a `.csv` for offline use or record-keeping.

---

## 🛠️ How It Works

1. **Upload** your student dataset via the sidebar (supporting CSV and Excel).
2. **Clean & Process** — the app automatically handles missing data and formats inputs for smooth analysis.
3. **Filter** using intuitive controls in the "Control Panel" sidebar—data and visuals update instantly.
4. **Visualize** your insights in the "Analytics Dashboard" with interactive charts and heatmaps.
5. **Interact & Communicate** — select students, compose emails, and preview your messages all within the app.

---

## 📁 Sample Data Format

To get started quickly, you can use the included sample dataset or prepare your own file with a similar structure. The app expects the following columns (case-insensitive):

| Column Name | Description                               | Example Values                                              |
| ----------- | ----------------------------------------- | ----------------------------------------------------------- |
| Name        | Full name of the student                  | "Aarav Patel", "Neha Shah"                                  |
| Email       | Student's email address                   | "[aarav.patel@example.com](mailto:aarav.patel@example.com)" |
| Branch      | Academic branch or department             | "Computer Science", "Mechanical"                            |
| Year        | Year of study                             | 1, 2, 3, 4                                                  |
| Interests   | Comma-separated list of interests/hobbies | "Music, Football, Coding"                                   |

**Note:**

* The `Interests` column can have multiple interests separated by commas.
* The app automatically handles missing or malformed data gracefully.

You can find the sample dataset in the repository as:
`sample_student_data.csv`

---

## ⚡ Built with Streamlit

Powered by [Streamlit](https://streamlit.io/), a cutting-edge Python framework designed to transform data scripts into beautiful, shareable web apps in minutes—no front-end experience required. Streamlit enables rapid prototyping and seamless interaction, making your data come alive with minimal code.

---

## 🤖 AI powered Features

✨ Newly Integrated Feature – The dashboard now comes with Generative AI capabilities to create highly personalized and professional emails instantly!

With Google Gemini API seamlessly integrated, you can:

Auto-generate personalized student emails based on selected data (branch, year, interests, etc.).

Customize tone — formal, friendly, or persuasive — in one click.

Preview before sending, ensuring your outreach stays relevant and engaging.

Save time and increase response rates by avoiding manual drafting.

---

<img width="2880" height="1286" alt="pic1" src="https://github.com/user-attachments/assets/0ee95577-bf57-4921-bfb5-9b2485a1911b" />

---

<img width="2878" height="1286" alt="pic2" src="https://github.com/user-attachments/assets/f6735538-edbd-4a64-aa6d-8c4bd29a0607" />

---

<img width="2880" height="1274" alt="pic3" src="https://github.com/user-attachments/assets/9950d125-5ec5-43fd-b60d-1c5722065f92" />

---

<img width="2880" height="1278" alt="pic3 1" src="https://github.com/user-attachments/assets/c7b991bd-6a7e-438b-8ae5-157cadc1090c" />

---

<img width="2880" height="1280" alt="pic4" src="https://github.com/user-attachments/assets/2e8f8900-a9de-4b49-bce3-d8d43beab5cb" />

---

<img width="2880" height="1270" alt="pic5" src="https://github.com/user-attachments/assets/74c4f311-db29-4181-8ccc-a3bd338044f9" />

---

<img width="2870" height="1262" alt="pic6" src="https://github.com/user-attachments/assets/4a9b2ec6-29d4-4fd2-ab13-e20a7a9553d9" />

---

---
### 🎥 Watch the Live Demo

Check out this quick video walkthrough of the **Insight Deck Dashboard** to see all the features in action, from uploading data to generating real-time analytics.

[Insight Deck Dashboard Demo](https://drive.google.com/file/d/12TNrt9id3BTsfQLvf75CULWjmC6HyBoU/view?usp=sharing)

*Click the above link to watch the video.*

---

Feel free to explore, contribute, and help us build the future of student data interaction!
