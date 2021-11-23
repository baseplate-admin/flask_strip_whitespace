# Thanks to
# https://stackoverflow.com/questions/67563385/how-do-i-access-response-content-in-wsgi-middleware-for-flask
# I got this middleware working

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

from typing import Union
from werkzeug.wrappers import Request, Response


class HTMLStripWhiteSpaceMiddleware(object):
    def __init__(self, app):
        self.app = app

        # Declare the variables that we need as None.
        self.request: Request = None
        self.app_iter = None
        self.html = b""

        # Set Some modifiable variables

        self.STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE: bool
        self.STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES: bool
        self.STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS: bool
        self.STRIP_WHITESPACE_RUST_KEEP_COMMENTS: bool
        self.STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS: bool
        self.STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES: bool
        self.STRIP_WHITESPACE_RUST_MINIFY_CSS: bool
        self.STRIP_WHITESPACE_RUST_MINIFY_JS: bool
        self.STRIP_WHITESPACE_RUST_REMOVE_BANGS: bool = True
        self.STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS: bool = True
        # Python
        self.STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS: bool
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML: bool
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML: bool
        self.STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS: bool
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE: bool
        self.STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES: bool
        # NBSP char
        self.STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER: str
        # Compression Settings
        self.STRIP_WHITESPACE_COMPRESSION_TYPE: Union[
            str("compressed"), str("decompressed")
        ]
        self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM: Union[
            str("gzip"), str("br"), str("zstd"), str("plain")
        ]

    def __compress__(
        self,
        buffer: bytes,
    ) -> bytes:

        return_buffer: bytes = b""

        if self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM == str("gzip"):
            try:
                from python_strip_whitespace.functions.compressors.gzip import (
                    compress as gz_compress,
                )
            except ImportError:
                raise ImportError(
                    """
                    'gz_compress' function is missing

                        Did you install the latest python_strip_whitespace?
                        
                        If not install it by:
                            python -m pip install python_strip_whitespace
                    """
                )

            return_buffer = gz_compress(buffer)

        elif self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM == str("br"):
            try:
                from python_strip_whitespace.functions.compressors.brotli import (
                    compress as br_compress,
                )
            except ImportError:
                raise ImportError(
                    """
                    'br_compress' function is missing

                        Did you install the latest python_strip_whitespace?
                        
                        If not install it by:
                            python -m pip install python_strip_whitespace
                    """
                )

            return_buffer = br_compress(buffer)

        elif self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM == str("zstd"):

            try:
                from python_strip_whitespace.functions.compressors.zstd import (
                    compress as zstd_compress,
                )
            except ImportError:
                raise ImportError(
                    """
                    'zstd_compress' function is missing

                        Did you install the latest python_strip_whitespace?
                        
                        If not install it by:
                            python -m pip install python_strip_whitespace
                """
                )

            return_buffer = zstd_compress(buffer)
        else:
            raise AttributeError

        return return_buffer

    def __map_environ_to_variables__(self, environ: dict):
        """
        This module maps flask's environment variables to self
            :params environ
        """
        self.STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE = environ.get(
            "STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE", True
        )
        self.STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES = (
            environ.get(
                "STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES",
                True,
            )
        )
        self.STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS = environ.get(
            "STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS", True
        )
        self.STRIP_WHITESPACE_RUST_KEEP_COMMENTS = environ.get(
            "STRIP_WHITESPACE_RUST_KEEP_COMMENTS", True
        )
        self.STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS = environ.get(
            "STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS", True
        )
        self.STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES = environ.get(
            "STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES", True
        )
        self.STRIP_WHITESPACE_RUST_MINIFY_CSS = environ.get(
            "STRIP_WHITESPACE_RUST_MINIFY_CSS", True
        )
        self.STRIP_WHITESPACE_RUST_MINIFY_JS = environ.get(
            "STRIP_WHITESPACE_RUST_MINIFY_JS", True
        )
        self.STRIP_WHITESPACE_RUST_REMOVE_BANGS = environ.get(
            "STRIP_WHITESPACE_RUST_REMOVE_BANGS", True
        )
        self.STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS = environ.get(
            "STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS", True
        )

        self.STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS = environ.get(
            "STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS",
            False,  # We do it in Rust. No need to do it in python
        )
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML = environ.get(
            "STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML", True
        )
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML = environ.get(
            "STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML", True
        )
        self.STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS = environ.get(
            "STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS", True
        )
        self.STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE = environ.get(
            "STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE", True
        )
        self.STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES = environ.get(
            "STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES", True
        )
        self.STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER = environ.get(
            "STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER", "অ"
        )
        self.STRIP_WHITESPACE_COMPRESSION_TYPE = environ.get(
            "STRIP_WHITESPACE_COMPRESSION_TYPE", str("decompressed")
        )
        self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM = environ.get(
            "STRIP_WHITESPACE_COMPRESSION_ALGORITHM",
            str(
                "gzip",  # By default set it to GZ because its a python stdlib
            ),
        )

    def __call__(self, environ, start_response):
        self.request: Request = Request(environ)
        self.__map_environ_to_variables__(environ)

        def custom_start_response(status, headers, exc_info=None):
            accepted_encodings = self.request.headers.get(
                "Accept-Encoding", ""  # Has gzip, deflate by default
            )

            if self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM == str("plain"):
                # If algorithm is text/plain rdon't do anything
                headers.append(
                    (
                        "Content-Encoding",
                        "text/plain; charset:utf-8",
                    )
                )

            elif (
                self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM != str("plain")
                and self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM in accepted_encodings
            ):
                headers.append(
                    (
                        "Content-Encoding",
                        str(self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM),
                    )
                )

            else:
                raise ValueError(
                    f"""
                    'algorithm' in 'strip_whitespace.add_header' must be one of these four.
                        1. gzip
                        2. br ( Brotli )
                        3. zstd ( ZStandard )
                        4. plain ( Decompressed HTML )

                    Currently algorithm is: { self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM }
                    """
                )
            return start_response(status, headers, exc_info)

        self.app_iter = self.app(environ, custom_start_response)
        self.html = b"".join(self.app_iter)

        body: bytes = minify_html(
            self.html,
            self.STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE,
            self.STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES,
            self.STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS,
            self.STRIP_WHITESPACE_RUST_KEEP_COMMENTS,
            self.STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS,
            self.STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES,
            self.STRIP_WHITESPACE_RUST_MINIFY_CSS,
            self.STRIP_WHITESPACE_RUST_MINIFY_JS,
            self.STRIP_WHITESPACE_RUST_REMOVE_BANGS,
            self.STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS,
            # Python
            self.STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS,
            self.STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML,
            self.STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML,
            self.STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS,
            self.STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE,
            self.STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES,
            # NBSP char
            self.STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER,
            # Compression Settings
            self.STRIP_WHITESPACE_COMPRESSION_TYPE,
        )
        body = self.__compress__(body)

        return [body]
