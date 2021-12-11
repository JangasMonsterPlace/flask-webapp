from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__,
    static_folder='static/',
    template_folder='templates/'
)


@app.route("/")
def hello_world():
    return "<p>Let's create an awesome app!!</p>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
