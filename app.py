from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("career_prediction_model.pkl")

# Load skill columns
skill_columns = joblib.load("skill_columns.pkl")

# Required skills for each career
career_skills = {
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power_BI",
        "Statistics", "Pandas", "Data_Visualization"
    ],

    "Data Scientist": [
        "Python", "SQL", "Statistics", "Pandas",
        "Machine_Learning", "Data_Visualization"
    ],

    "ML Engineer": [
        "Python", "Machine_Learning", "Pandas",
        "Statistics", "Git", "Java"
    ],

    "Business Analyst": [
        "Excel", "SQL", "Statistics",
        "Power_BI", "Communication", "Data_Visualization"
    ],

    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React", "Git"
    ],

    "Backend Developer": [
        "Python", "Java", "SQL", "Git", "Communication"
    ]
}


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # Get selected skills
        user_skills = request.form.getlist("skills")

        # Convert skills into 0/1 values
        input_data = []

        for skill in skill_columns:
            if skill in user_skills:
                input_data.append(1)
            else:
                input_data.append(0)

        # Create DataFrame
        input_df = pd.DataFrame(
            [input_data],
            columns=skill_columns
        )

        # Predict career
        predicted_career = model.predict(input_df)[0]

        # Get required skills
        required_skills = career_skills[predicted_career]

        # Find missing skills
        missing_skills = [
            skill
            for skill in required_skills
            if skill not in user_skills
        ]

        return render_template(
            "index.html",
            skills=skill_columns,
            result=predicted_career,
            missing_skills=missing_skills
        )

    return render_template(
        "index.html",
        skills=skill_columns
    )


if __name__ == "__main__":
    app.run(debug=True)