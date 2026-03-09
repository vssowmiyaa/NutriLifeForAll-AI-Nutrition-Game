from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
data = pd.read_csv("dataset.csv")

# Store previous scores
scores = []

# Home page
@app.route('/')
def home():
    return render_template("index.html")


# Ingredient selection page
@app.route('/ingredient')
def ingredient():
    return render_template("ingredient.html")


# Login page
@app.route('/login')
def login():
    return render_template("login.html")


# How to play page
@app.route('/howtoplay')
def howtoplay():
    return render_template("howtoplay.html")


# Dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", scores=scores)


# Analyze ingredients
@app.route('/analyze', methods=['POST'])
def analyze():

    ingredients = request.form.getlist('ingredient')

    total_calories = 0
    total_co2 = 0
    total_water = 0
    total_waste = 0

    for ing in ingredients:

        row = data[data['ingredient'] == ing].iloc[0]

        total_calories += row['calories']
        total_co2 += row['co2']
        total_water += row['water']
        total_waste += row['waste']

    health = 100 - (total_calories / 2)
    growth = 80 - total_co2
    sustainability = 100 - (total_co2 + total_water/50 + total_waste)

    score = {
        "ingredients": ", ".join(ingredients),
        "health": round(health),
        "growth": round(growth),
        "sustainability": round(sustainability)
    }

    scores.append(score)

    return render_template(
        "analysis.html",
        ingredients=", ".join(ingredients),
        calories=total_calories,
        co2=total_co2,
        water=total_water,
        waste=total_waste,
        health=round(health),
        growth=round(growth),
        sustainability=round(sustainability)
    )

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
