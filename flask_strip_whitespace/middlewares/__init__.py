from typing import (
    Any,
    Dict,
    List,
)

try:
    from python_strip_whitespace import minify_html
except ImportError:
    raise ImportError(
        """
        'minify_html' function missing
            Did you install the latest python_strip_whitespace?
            
                First uninstall it by:
                    python -m pip uninstall python_strip_whitespace
                
                If not install it by:
                    python -m pip install python_strip_whitespace
        """
    )


class HTMLStripWhiteSpaceMiddleware(object):
    def __init__(self, app, config: Dict[str, Any] = {}):
        self.app = app

        # Set Some modifiable variables
        ## RUST

        self.STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE: bool = config.get(
            "STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE", True
        )
        self.STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES: bool = config.get(
            "STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES",
            True,
        )
        self.STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS: bool = config.get(
            "STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS", True
        )
        self.STRIP_WHITESPACE_RUST_KEEP_COMMENTS: bool = config.get(
            "STRIP_WHITESPACE_RUST_KEEP_COMMENTS", True
        )
        self.STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS: bool = config.get(
            "STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS", True
        )
        self.STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES: bool = config.get(
            "STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES", True
        )
        self.STRIP_WHITESPACE_RUST_MINIFY_CSS: bool = config.get(
            "STRIP_WHITESPACE_RUST_MINIFY_CSS", True
        )
        self.STRIP_WHITESPACE_RUST_MINIFY_JS: bool = config.get(
            "STRIP_WHITESPACE_RUST_MINIFY_JS", True
        )
        self.STRIP_WHITESPACE_RUST_REMOVE_BANGS: bool = config.get(
            "STRIP_WHITESPACE_RUST_REMOVE_BANGS", True
        )
        self.STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS: bool = config.get(
            "STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS", True
        )

        ## Python

        self.STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS: bool = config.get(
            "STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS",
            False,  # We do it in Rust. No need to do it in python
        )
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML: bool = config.get(
            "STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML", True
        )
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML: bool = config.get(
            "STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML", True
        )
        self.STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS: bool = config.get(
            "STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS", True
        )
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE: bool = config.get(
            "STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE", True
        )
        self.STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES: bool = config.get(
            "STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES", True
        )

        ## NBSP char

        self.STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER: str = config.get(
            "STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER", "'অ'"
        )

        ## Compression Settings

        self.STRIP_WHITESPACE_COMPRESSION_TYPE: str = config.get(
            "STRIP_WHITESPACE_COMPRESSION_TYPE", str("decompressed")
        )

        self.STRIP_WHITESPACE_REGEX_FLAVOR: str = config.get(
            "STRIP_WHITESPACE_REGEX_FLAVOR", str("plain")
        )

        ## Ignored paths

        self.STRIP_WHITESPACE_MINIFY_IGNORED_PATHS: List = config.get(
            "STRIP_WHITESPACE_COMPRESSION_ALGORITHM",
            [
                "/favicon.ico",
            ],
        )

    def __call__(self, environ: dict, start_response) -> List[bytes]:
        app_iter = self.app(environ, start_response)
        body: bytes = minify_html(
            b"".join(app_iter).decode("utf8"),
            STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE=self.STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE,
            STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES=self.STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES,
            STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS=self.STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS,
            STRIP_WHITESPACE_RUST_KEEP_COMMENTS=self.STRIP_WHITESPACE_RUST_KEEP_COMMENTS,
            STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS=self.STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS,
            STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES=self.STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES,
            STRIP_WHITESPACE_RUST_MINIFY_CSS=self.STRIP_WHITESPACE_RUST_MINIFY_CSS,
            STRIP_WHITESPACE_RUST_MINIFY_JS=self.STRIP_WHITESPACE_RUST_MINIFY_JS,
            STRIP_WHITESPACE_RUST_REMOVE_BANGS=self.STRIP_WHITESPACE_RUST_REMOVE_BANGS,
            STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS=self.STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS,
            # Python
            STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS=self.STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS,
            STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML=self.STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML,
            STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML=self.STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML,
            STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS=self.STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS,
            STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE=self.STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE,
            STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES=self.STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES,
            # NBSP char
            STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER=self.STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER,
            # Compression Settings
            STRIP_WHITESPACE_REGEX_FLAVOR=self.STRIP_WHITESPACE_REGEX_FLAVOR,
        )

        return [body]
