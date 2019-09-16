from flask import Flask, render_template

# Create web server
app = Flask(__name__)

# route needs to be made to figure out location


@app.route("/")  # root route lmao
def home():
    return render_template('index.html')


# Another route
@app.route("/about")
def pred():
    return render_template('about.html')
# Routes do not have to be functions, usually use template

if __name__ == "__main__":
    app.run(debug=True)
