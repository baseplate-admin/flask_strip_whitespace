from flask import Flask
from flask_strip_whitespace.middlewares import HTMLStripWhiteSpaceMiddleware


app = Flask(__name__)

#   Declare The configuration dictionary.
#   Modify any of them as you please.
#   Docs over at : https://github.com/baseplate-admin/flask_strip_whitespace#customization-
#   Good luck.
STRIP_WHITESPACE_CONFIG: dict = {
    ## Rust
    # "STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE": True,  # passes do_not_minify_doctype to minify-html
    # "STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES": True,  # passes ensure_spec_compliant_unquoted_attribute_values to minify-html
    # "STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS": True,  # passes keep_closing_tags to minify-html
    # "STRIP_WHITESPACE_RUST_KEEP_COMMENTS": True,  # passes keep_comments to minify-html
    # "STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS": True,  # passes keep_html_and_head_opening_tags to minify-html
    # "STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES": True,  # passes keep_spaces_between_attributes to minify-html
    # "STRIP_WHITESPACE_RUST_MINIFY_CSS": True,  # passes minify_css to minify-html
    # "STRIP_WHITESPACE_RUST_MINIFY_JS": True,  # passes minify_js to minify-html
    # "STRIP_WHITESPACE_RUST_REMOVE_BANGS": True,  # passes remove_bangs to minify-html
    # "STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS": True,  # passes remove_processing_instructions to minify-html
    ## Python
    # "STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS": False,  # removes comments from HTML using python ( not recommended cause rust can do that just fine and fast )
    # "STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML": True,  # replaces '<style text/css>' -> '<style>'
    # "STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML": True,  # replaces '<script text/javascript>' -> '<script>'
    # "STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS": True,  # removes some unnecessary tags
    # "STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE": True,  # This is where the magic happens.
    # "STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES": True,  # This is also a magic module.
    # "STRIP_WHITESPACE_MINIFY_IGNORED_PATHS": [],  # Note that STRIP_WHITESPACE_MINIFY_IGNORED_PATHS is a Python List
}

app.wsgi_app = HTMLStripWhiteSpaceMiddleware(
    app.wsgi_app, config=STRIP_WHITESPACE_CONFIG
)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.run(debug=True)
