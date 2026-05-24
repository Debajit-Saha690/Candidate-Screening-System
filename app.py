import random
from flask import Response, request
from flask import Flask, render_template, request, redirect, session
from db import get_connection

app = Flask(__name__)
app.secret_key = "a9f8d2c1e7b4f6g3h5j8k2l9"

# EXPERIENCE CONVERTER

def convert_experience(exp_input):
    exp_input = exp_input.lower().strip()

    if exp_input == "na":
        return 0

    parts = exp_input.split()
    if len(parts) != 2:
        return None

    try:
        number = float(parts[0])
    except:
        return None

    unit = parts[1]

    if unit in ["year", "years"]:
        return number * 12
    elif unit in ["month", "months"]:
        return number

    return None


# CODING AVERAGE (weighted)

def coding_average(c):
    return round(
        (c["leetcode"] * 0.4 +
         c["codechef"] * 0.3 +
         c["hackerrank"] * 0.3),
        2
    )


# RANKING SCORE 

def calculate_score(c):

    coding = coding_average(c)
    class10 = c["class10"]
    class12 = c["class12"]
    cgpa = c["cgpa"]
    projects = c["projects"]
    hackathons = c["hackathons_count"]
    experience = c["experience"]

    # cap experience to avoid unfair scaling
    experience = min(experience, 24)

    score = (
        (c["class10"] * 0.10) +
        (c["class12"] * 0.10) +
        (c["cgpa"] * 10 * 0.35) +          # academics
        (coding * 0.25) +                  # coding platforms
        (c["projects"] * 0.15) +           # projects
        (c["hackathons_count"] * 0.10) +   # hackathons
        (experience * 0.1)                 # experience
    )

    return round(score, 2)

# SCORE BREAKDOWN (Explainable scoring)

def score_breakdown(c):
    coding = coding_average(c)
    academic = round(
        (c["class10"] * 0.10) +
        (c["class12"] * 0.10) +
        (c["cgpa"] * 10 * 0.35),
        2
    )
    coding_part = round(coding * 0.25, 2)
    project_part = round(c["projects"] * 0.15, 2)
    hackathon_part = round(c["hackathons_count"] * 0.10, 2)

    exp = min(c["experience"], 24)
    exp_part = round(exp * 0.1, 2)

    return {
        "academic": academic,
        "coding": coding_part,
        "projects": project_part,
        "hackathons": hackathon_part,
        "experience": exp_part
    }


# SKILL BOOST 

def apply_skill_boost(c, required_skills):
    if not required_skills:
        return
    
    candidate_skills = (
        c["skills"] if isinstance(c["skills"], list)
        else [s.strip().lower() for s in c["skills"].split(",")]
    )

    match_count = len(set(required_skills) & set(candidate_skills))
    c["skill_match"] = match_count
    c["score"] += match_count * 1


# REASON FOR SELECTION 

def generate_selection_reason(c):

    reasons = []

    # Academic strength
    if c["cgpa"] >= 8:
        reasons.append("Strong CGPA performance")

    if c["class10"] >= 75:
        reasons.append("Good Class 10 academic record")

    if c["class12"] >= 75:
        reasons.append("Good Class 12 academic record")

    # Coding strength
    if c["coding_avg"] >= 75:
        reasons.append("Excellent coding performance")

    elif c["coding_avg"] >= 60:
        reasons.append("Good coding performance")

    # Projects
    if c["projects"] >= 2:
        reasons.append("Strong project experience")
    elif c["projects"] == 1:
        reasons.append("Some project experience")

    # Hackathons
    if c["hackathons_count"] >= 1:
        reasons.append("Hackathon participation")

    # Skills
    if c.get("skill_match", 0) >= 2:
        reasons.append("Good skill alignment with requirements")

    # Experience
    if c.get("experience", 0) > 0:
        reasons.append("Relevant experience added value")

    if len(reasons) == 0:
        return "Meets required selection criteria"

    return ", ".join(reasons)


# REASON FOR REJECTION

def generate_rejection_reason(c, required_skills=None, min_score=0):

    reasons = []

    # Academic checks
    if c["class10"] < 60:
        reasons.append("Low Class 10 marks")

    if c["class12"] < 60:
        reasons.append("Low Class 12 marks")

    if c["cgpa"] < 6:
        reasons.append("Low CGPA")

    # Projects
    if c["projects"] == 0:
        reasons.append("No project experience")

    # Hackathons
    if c["hackathons_count"] == 0:
        reasons.append("No hackathon participation")

    # Coding
    if c["coding_avg"] < 50:
        reasons.append("Weak coding performance")

    # Score cutoff
    if c["score"] < min_score:
        reasons.append("Below required placement score")

    # Skills check
    if required_skills:
        candidate_skills = (
            c["skills"] if isinstance(c["skills"], list)
            else [s.strip().lower() for s in c["skills"].split(",") if s.strip()]
        )

        if len(set(required_skills) & set(candidate_skills)) == 0:
            reasons.append("No matching skills")

    if len(reasons) == 0:
        return "Did not meet selection threshold"

    return ", ".join(reasons)

# Tags for Candidates
def generate_tags(c, status):

    tags = []

    if status == "selected":

        if c["cgpa"] >= 8:
            tags.append("Strong Academics")

        if c["coding_avg"] >= 75:
            tags.append("Strong Coding")

        if c["hackathons_count"] > 0:
            tags.append("Hackathon Active")

        if c["projects"] >= 2:
            tags.append("Project Builder")

        if c["experience"] == 0:
            tags.append("Fresher")

        if c["score"] >= 75:
            tags.append("High Score")

    else:
        if c["cgpa"] < 6:
            tags.append("Weak Academics")
        
        if c["skill_match"] == 0:
            tags.append("No Skill Match")

        if c["score"] < 60:
            tags.append("Low Score")

    return tags

# RANKING BADGES FOR CANDIDATES BASED ON PLACEMENT SCORE 
def get_badge(score):
    if score >= 80:
        return "🥇 Top Performer"
    elif score >= 70:
        return "🥈 Strong Candidate"
    elif score >= 60:
        return "🥉 Average Candidate"
    else:
        return "❌ Below Threshold"

@app.route("/")
def root():
    return render_template("home.html")


@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if session.get("admin"):
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin@2k28":
            session["admin"] = True

            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)

            return redirect("/")

        return "Invalid Credentials"

    return render_template("admin_login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ADD CANDIDATE

@app.route("/add", methods=["GET", "POST"])
def add_candidate():

    if not session.get("admin"):
        return redirect("/admin?next=/add")
    
    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        # ID generation 
        cursor.execute("SELECT MAX(id) FROM candidates")
        max_id = cursor.fetchone()[0]
        if max_id is None:
            app_id = 1000
        else:
            app_id = max_id + 1

        exp_input = request.form.get("experience", "NA")
        experience = convert_experience(exp_input)

        if experience is None:
            return "Invalid Experience Format (use '2 years' or '6 months' or 'NA')"
        
        skills = ",".join([
            s.strip().lower()
            for s in request.form.get("skills", "").split(",")
            if s.strip()
        ])

        query = """
        INSERT INTO candidates (
            id, name, class10, class12, cgpa,
            projects, hackathons_count, hackathon_position,
            leetcode, codechef, hackerrank,
            skills, experience, experience_input
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            app_id,
            request.form["name"],
            float(request.form["class10"]),
            float(request.form["class12"]),
            float(request.form["cgpa"]),
            int(request.form["projects"]),
            int(request.form["hackathons_count"]),
            request.form["hackathon_position"],
            int(request.form["leetcode"]),
            int(request.form["codechef"]),
            int(request.form["hackerrank"]),
            skills,
            experience,
            exp_input
        )

        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return redirect("/view")

    return render_template("add.html")


# VIEW ALL (RANKED)

@app.route("/view")
def view():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()

    for c in candidates:
        c["skills"] = [s.strip().lower() for s in c["skills"].split(",")] if c["skills"] else []
        c["coding_avg"] = coding_average(c)
        c["score"] = calculate_score(c)
        c["breakdown"] = score_breakdown(c)

    candidates.sort(key=lambda x: x["score"], reverse=True)

    for i, c in enumerate(candidates, start=1):
        c["rank"] = i

    conn.close()
    return render_template("view.html", candidates=candidates)


# SEARCH

@app.route("/search", methods=["GET", "POST"])
def search():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    result = None
    results = []
    message = None

    if request.method == "POST":

        search_type = request.form["search_type"]
        value = request.form["search_value"]

        if search_type == "id":
            cursor.execute("SELECT * FROM candidates WHERE id=%s", (value,))
            result = cursor.fetchone()

            if result:
                result["coding_avg"] = coding_average(result)
                result["score"] = calculate_score(result)
                result["breakdown"] = score_breakdown(result)

                result["skills"] = [
                    s.strip().title()
                    for s in result["skills"].split(",")
                    if s.strip()
                ]

        else:
            cursor.execute(
                "SELECT * FROM candidates WHERE name LIKE %s",
                ("%" + value + "%",)
            )
            results = cursor.fetchall()

            for r in results:
                r["coding_avg"] = coding_average(r)
                r["score"] = calculate_score(r)
                r["breakdown"] = score_breakdown(r)

                r["skills"] = [
                    s.strip().title()
                    for s in r["skills"].split(",")
                    if s.strip()
                ]

        if not result and not results:
            message = "No Candidate Found"

    conn.close()
    return render_template("search.html", result=result, results=results, message=message)


# FILTER + RANK

@app.route("/filter", methods=["GET", "POST"])
def filter_candidates():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()

    selected = []
    rejected = []
    report = None

    if request.method == "POST":

        min_class10 = float(request.form.get("min_class10", 0))
        min_class12 = float(request.form.get("min_class12", 0))
        min_cgpa = float(request.form.get("min_cgpa", 0))
        min_projects = int(request.form.get("min_projects", 0))
        min_hackathons = int(request.form.get("min_hackathons", 0))
        min_coding_score = float(request.form.get("min_coding_score", 0))

        required_skills = [s.strip().lower() for s in request.form.get("skills", "").split(",") if s.strip()]
        skills_count = len(required_skills)
        min_exp = convert_experience(request.form.get("min_exp"))

        company_level = request.form.get("company_level")
        
        if company_level == "easy":
            min_score = 60
        elif company_level == "medium":
            min_score = 70
        elif company_level == "hard":
            min_score = 80
        else:
            min_score = 60

        for c in candidates:

            # Normalize skills first
            c["skills"] = [s.strip().lower() for s in c["skills"].split(",")] if c["skills"] else []

            # Corrected experience conversion
            c["exp_months"] = convert_experience(c.get("experience_input", "NA")) or 0

            # base calculations
            c["coding_avg"] = coding_average(c)
            c["score"] = calculate_score(c)

            # ranking badges
            c["badge"] = get_badge(c["score"])

            # score breakdown after final score
            c["breakdown"] = score_breakdown(c)

            candidate_skills = (
                c["skills"] if isinstance(c["skills"], list)
                else [s.strip().lower() for s in c["skills"].split(",")]
            )
            c["skill_match"] = len(set(required_skills) & set(candidate_skills))

            # skill boost
            apply_skill_boost(c, required_skills)

            winner_required = request.form.get("winner_required", "no")
            if winner_required == "yes":
                if c["hackathon_position"] and str(c["hackathon_position"]).lower() in ["1", "winner", "first"]:
                    c["score"] += 5
                else:
                    rejected.append(c)
                    continue

            # filtering
            is_selected = (
                c["class10"] >= min_class10 and
                c["class12"] >= min_class12 and
                c["cgpa"] >= min_cgpa and
                c["projects"] >= min_projects and
                c["hackathons_count"] >= min_hackathons and
                c["coding_avg"] >= min_coding_score and
                c["score"] >= min_score and
                (min_exp is None or c["exp_months"] >= min_exp) and
                c["skill_match"] > 0  
            )
            if is_selected:
                c["breakdown"] = score_breakdown(c)
                c["reason"] = generate_selection_reason(c)
                c["tags"] = generate_tags(c, "selected")
                selected.append(c)
            else:
                c["breakdown"] = score_breakdown(c)
                c["reason"] = generate_rejection_reason(c, required_skills, min_score)
                c["tags"] = generate_tags(c, "rejected")
                rejected.append(c)
            
        # SORT selected candidates
        selected.sort(key=lambda x: x["score"], reverse=True)

        # ASSIGN RANKS
        for i, c in enumerate(selected, start=1):
            c["rank"] = i

        # SORT rejected candidates
        rejected.sort(key=lambda x: x["score"], reverse=True)

        # ASIGN RANKS
        for i, c in enumerate(rejected, start=1):
            c["rank"] = i

        # REPORT
        report = {
            "total": len(candidates),
            "selected": len(selected),
            "rejected": len(rejected),
            "company_level": company_level,
            "min_score": min_score
        }
        app.config["last_selected"] = selected
        app.config["last_rejected"] = rejected
        app.config["last_report"] = report
        conn.close()
        return redirect("/filter_result")
    conn.close()
    return render_template("filter.html")

@app.route("/filter_result")
def filter_result_page():

    selected = app.config.get("last_selected", [])
    rejected = app.config.get("last_rejected", [])
    report = app.config.get("last_report")

    if not report:
        return redirect("/filter")

    return render_template(
        "filter_result.html",
        selected=selected,
        rejected=rejected,
        report=report,
        company_level="",
        min_score=0)


@app.route("/selected")
def selected_page():

    data = app.config.get("last_selected", [])
    report = app.config.get("last_report", {
        "total": len(data),
        "selected": len(data),
        "rejected": 0
    })

    return render_template(
        "selected.html",
        selected=data,
        report=report)


@app.route("/rejected")
def rejected_page():

    data = app.config.get("last_rejected", [])
    report = app.config.get("last_report", {
        "total": 0,
        "selected": 0,
        "rejected": len(data)
    })

    return render_template(
        "rejected.html",
        rejected=data,
        report=report)


# PDF EXPORT

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import Table
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from io import BytesIO


def generate_pdf(data, title_text):

    buffer = BytesIO()

    # LANDSCAPE PDF
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=15,
        rightMargin=15,
        topMargin=20,
        bottomMargin=20
    )

    elements = []

    styles = getSampleStyleSheet()

    # SMALL TEXT STYLE
    body_style = ParagraphStyle(
        'body',
        parent=styles['BodyText'],
        fontSize=7,
        leading=9,
        alignment=TA_LEFT
    )

    # TITLE
    title = Paragraph(title_text, styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 10))

    # TABLE HEADER
    table_data = [[
        "Rank",
        "Name",
        "Score",
        "Coding Avg",
        "CGPA",
        "Projects",
        "Hackathons",
        "Skills",
        "Experience",
        "Tags",
        "Reason"
    ]]

    # TABLE ROWS
    for c in data:

        skills = c.get("skills", [])
        if isinstance(skills, list):
            skills = ", ".join(skills)

        tags = c.get("tags", [])
        if isinstance(tags, list):
            tags = ", ".join(tags)

        row = [
            Paragraph(str(c.get("rank", "")), body_style),
            Paragraph(str(c.get("name", "")), body_style),
            Paragraph(str(c.get("score", "")), body_style),
            Paragraph(str(c.get("coding_avg", "")), body_style),
            Paragraph(str(c.get("cgpa", "")), body_style),
            Paragraph(str(c.get("projects", "")), body_style),
            Paragraph(str(c.get("hackathons_count", "")), body_style),
            Paragraph(skills, body_style),
            Paragraph(str(c.get("exp_months", 0)), body_style),
            Paragraph(tags, body_style),
            Paragraph(c.get("reason", ""), body_style)
        ]

        table_data.append(row)

    # COLUMN WIDTHS
    col_widths = [
        30,   # Rank
        60,   # Name
        37,   # Score
        53,   # Coding Avg
        37,   # CGPA
        40,   # Projects
        54,   # Hackathons
        90,  # Skills
        52,   # Experience
        100,  # Tags
        180   # Reason
    ]

    # CREATE TABLE
    table = Table(
        table_data,
        colWidths=col_widths,
        repeatRows=1
    )

    # TABLE STYLE
    table.setStyle(TableStyle([

        # HEADER
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),

        # BODY
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),

        # GRID
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        # ALIGNMENT
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),

        # PADDING
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),

        # ROW COLORS
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

    ]))

    elements.append(table)

    # BUILD PDF
    pdf.build(elements)
    buffer.seek(0)
    return buffer

@app.route("/export_selected_pdf")
def export_selected_pdf():

    data = app.config.get("last_selected", [])

    if not data:
        return "No data available. Please apply filter first."

    pdf_buffer = generate_pdf(data, "Selected Candidates Report")

    return Response(
        pdf_buffer,
        mimetype='application/pdf',
        headers={
            'Content-Disposition':
            'attachment; filename=selected_candidates.pdf'
        }
    )

@app.route("/export_rejected_pdf")
def export_rejected_pdf():

    data = app.config.get("last_rejected", [])

    if not data:
        return "No data available. Please apply filter first."

    pdf_buffer = generate_pdf(data, "Rejected Candidates Report")

    return Response(
        pdf_buffer,
        mimetype='application/pdf',
        headers={
            'Content-Disposition':
            'attachment; filename=rejected_candidates.pdf'
        }
    )

# RUN APP

if __name__ == "__main__":
    app.run(debug=True, port=5001)
