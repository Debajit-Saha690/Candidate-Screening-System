# Candidate Screening & Ranking System

A web-based mini **Applicant Tracking System (ATS)** built using Flask and MySQL that evaluates, filters, and ranks candidates based on multiple performance metrics.

This project is designed to simulate a real-world campus placement screening process, where recruiters can efficiently shortlist candidates using customizable criteria.

---

## 🚀 Features

- 🔐 **Admin Login System**
- ➕ Add candidate details (academics, coding profiles, skills, experience)
- 📊 **Smart Scoring Algorithm**
  - Academic performance (10th, 12th, CGPA)
  - Coding platform scores (LeetCode, CodeChef, HackerRank)
  - Projects & Hackathons
  - Experience (converted into months)
- 🧠 **Explainable AI-like System**
  - Score breakdown
  - Selection & rejection reasons
- 🎯 **Advanced Filtering**
  - Custom criteria (marks, coding, skills, experience)
  - Company-level difficulty (Easy / Medium / Hard)
- 🏆 **Ranking System**
  - Rank-wise sorted candidates
  - Badges (Top Performer, Strong Candidate, etc.)
- 🏷️ Smart Tags (e.g., Strong Academics, Hackathon Active)
- 📈 **Visualization**
  - Bar Graph for selection vs rejection
- 📁 Export results to CSV (Selected & Rejected separately)

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** MySQL
- **Frontend:** HTML, CSS, Jinja2
- **Visualization:** Chart.js

---

## ⚙️ How It Works

1. Admin logs in and adds candidate data  
2. System calculates a **placement score** using weighted logic  
3. Recruiter applies filters based on requirements  
4. Candidates are:
   - ✅ Selected (ranked + explained)
   - ❌ Rejected (with reasons)
5. Results are visualized and can be exported  

---

## 📊 Scoring Logic (Simplified)

- Academics → 55%
- Coding Profiles → 25%
- Projects → 15%
- Hackathons → 10%
- Experience → Bonus (capped)

Also includes:
- Skill matching boost
- Hackathon winner bonus
- Company-level cutoff system

---

## 💡 Why I Built This

As a B.Tech CSE student, I wanted to understand how real placement systems work behind the scenes.  

This project helped me explore:

- Data-driven decision making  
- Backend system design using Flask  
- Database integration (MySQL)  
- Writing clean and modular logic  
- Building something useful for campus placements  

---

## 📷 Sample Output

- Ranked candidate list  
- Selection/rejection reasoning  
- Score breakdown  
- Visual analytics  

---

## ⭐ Final Note

This is a mini ATS built from scratch to simulate real placement workflows.  
Open to feedback and improvements 🚀

---

## Sreenshots

### Home Page
![Home](static/images/Home.png)

---

### Add Candidate Page
Candidate data entry form used to store academic details, coding profiles, skills, and experience into the system database.
![Add1](static/images/Add1.png)
![Add2](static/images/Add2.png)

---

### Filter Criteria Page
Custom filtering interface allowing recruiters to set minimum eligibility criteria such as academics, coding score, skills, and experience level.
![Filter1](static/images/Filter1.png)
![Filter2](static/images/Filter2.png)

---

### Filter Result Page
Final screening output showing selected and rejected candidates based on applied filtering criteria, along with scoring breakdown and ranking system.
![Filter_Rank1](static/images/Filter_Rank1.png)
Ranked list of top-performing candidates generated using a weighted scoring system based on academics, coding performance, projects, and experience.
![Filter_Rank2](static/images/Filter_Rank2.png)
![Filter_Rank3](static/images/Filter_Rank3.png)

---

### Pie Chart
Visual representation of selection vs rejection ratio using dynamic chart-based analytics for quick decision insights.
![Pie_Chart](static/images/Pie_Chart.png)
