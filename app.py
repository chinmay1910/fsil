from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/google-bert/bert-base-uncased"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_insights(text):
    payload = {"inputs": text}
    try:
        insights = query(payload)
        generated_text = insights.get("generated_text")
        if generated_text:
            return generated_text.strip()
        else:
            return "Failed to generate insights"
    except Exception as e:
        return f"Error: {e}"

# Function to extract text from downloaded filings
def extract_text_from_filings(ticker, output_dir):
    text = ""
    filings_dir = os.path.join(output_dir, ticker)

    for filename in os.listdir(filings_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(filings_dir, filename), "r") as file:
                text += file.read() + "\n"

    return text

# Function to generate and save a pie chart
def generate_pie_chart(labels, values, filename="static/pie_chart.png"):
    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Sentiment Distribution")
    plt.savefig(filename)
    plt.close()  # Close the figure to release resources

# Route for home page with form to enter company ticker
@app.route('/')
def index():
    return render_template('index.html')

# Route for analyzing company filings and displaying insights
@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        ticker = request.form['ticker']
        output_dir = "sec-edgar-filings"  # Directory containing the downloaded 10-K filings

        # Extract text from downloaded filings
        filings_text = extract_text_from_filings(ticker, output_dir)

        # Generate insights using Hugging Face API
        insights = generate_insights(filings_text)

        # Prepare data for visualization (example data)
        labels = ['Positive', 'Negative', 'Neutral']
        values = [30, 20, 50]  # Example values for sentiment distribution (replace with actual data)

        # Generate pie chart
        generate_pie_chart(labels, values, filename="static/pie_chart.png")

        # Render the result.html template with generated insights and visualization
        return render_template('result.html', ticker=ticker, insights=insights)

    return "Invalid request method"

if __name__ == '__main__':
    app.run(debug=True)
