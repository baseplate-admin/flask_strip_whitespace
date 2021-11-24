from flask import Flask
from flask_strip_whitespace.middlewares import HTMLStripWhiteSpaceMiddleware


app = Flask(__name__)

app.wsgi_app = HTMLStripWhiteSpaceMiddleware(
    app.wsgi_app,
    config={
         "STRIP_WHITESPACE_RUST_MINIFY_CSS": False,
         "STRIP_WHITESPACE_COMPRESSION_ALGORITHM": "plain",
     },
)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.run(debug=True)
