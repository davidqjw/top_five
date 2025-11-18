from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Simple in-memory storage for user submissions
# Each submission will contain: category, five items, and a timestamp
submissions = []

@app.route("/", methods=["GET", "POST"])
def home():
    global submissions
    if request.method == "POST":
        # Retrieve category and the five items from the POST form
        category = request.form.get("category", "").strip()
        items = [
            request.form.get(f"item{i}", "").strip() for i in range(1, 6)
        ]

        # Validate: category and all five items must be filled
        if category and all(items):
            submissions.append({
                "category": category,
                "five": items,
                # Add timestamp for the submission
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        # Redirect to homepage to avoid form resubmission on refresh
        return redirect(url_for("home"))

    # Render the homepage template with all current submissions
    return render_template("index.html", submissions=submissions)


# Route to delete a single submission by its index
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    global submissions
    if 0 <= index < len(submissions):
        del submissions[index]
    return redirect(url_for("home"))


# Route to clear all submissions
@app.route("/clear", methods=["POST"])
def clear():
    global submissions
    submissions.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
