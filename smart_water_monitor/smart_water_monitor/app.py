from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("water_quality_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    table = None

    if request.method == "POST":

        # DATASET UPLOAD
        if "dataset" in request.files:

            file = request.files["dataset"]

            if file.filename != "":

                data = pd.read_csv(file)

                predictions = model.predict(data)

                data["Result"] = [
                    "🟢 Safe"
                    if p == 1
                    else "🔴 Unsafe"
                    for p in predictions
                ]

                safe = (predictions == 1).sum()
                unsafe = (predictions == 0).sum()
                total = len(predictions)

                safe_percent = (safe / total) * 100

                if safe_percent >= 80:
                    result = """🟢 WATER IS SAFE """

                elif safe_percent >= 50:
                    result = "🟡 MIXED WATER QUALITY"
                  

                else:
                 result = "🔴 WATER IS UNSAFE"

                table = data.to_html(
                    classes="table",
                    index=False
                )

    return render_template(
        "index.html",
        result=result,
        table=table
    )


if __name__ == "__main__":
    app.run(debug=True)