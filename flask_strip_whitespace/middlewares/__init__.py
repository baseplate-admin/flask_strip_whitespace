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

from typing import Dict, List, Optional, Union
from werkzeug.wrappers import Request, Response
from flask import current_app


class HTMLStripWhiteSpaceMiddleware(object):
    def __init__(
        self,
        app,
        config: Optional[Dict[str, bool | str | List[str]]] = {},
    ) -> None:
        self.app = app

        # Declare the variables that we need as None.
        self.request: Request = None
        self.app_iter = None
        self.html = b""

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
            "STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER", "অ"
        )

        ## Compression Settings

        self.STRIP_WHITESPACE_COMPRESSION_TYPE: Union[
            str("compressed"), str("decompressed")
        ] = config.get("STRIP_WHITESPACE_COMPRESSION_TYPE", str("decompressed"))

        self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM: str("gzip") or str("br") or str(
            "zstd"
        ) or str("plain") = config.get(
            "STRIP_WHITESPACE_COMPRESSION_ALGORITHM",
            str("gzip"),  # By default set it to GZ because its a python stdlib
        )

        ## Ignored paths

        self.STRIP_WHITESPACE_MINIFY_IGNORED_PATHS: List = config.get(
            "STRIP_WHITESPACE_COMPRESSION_ALGORITHM",
            [
                "/favicon.ico",
            ],
        )

    def __compress__(self, buffer: bytes) -> bytes:

        algorithm = self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM
        # HTML should always be sent in bytes 🔢
        return_buffer: bytes = b""

        if algorithm == str("plain"):
            """
            If algorithm is text/plain don't do anything 🤷‍♂️
            """
            return_buffer = buffer

        elif algorithm == str("gzip"):
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

        elif algorithm == str("br"):
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

        elif algorithm == str("zstd"):
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
            raise AttributeError(
                f"""
                
                Error in 'strip_whitespace.middlewares.functions.compress_according_to_algorithm_choice'
                        Compression algorithm not any of these:
                            |> str("gzip")
                            |> str("br")
                            |> str("zstd")
                            |> str("plain")

                        Currently the Algorithm is : { algorithm }
                """
            )

        return return_buffer

    def __call__(self, environ: dict, start_response) -> Response:
        self.request: Request = Request(environ)

        def custom_start_response(status, headers, exc_info=None):

            algorithm = self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM
            accepted_encodings = self.request.headers.get(
                "Accept-Encoding", ""  # Has gzip, deflate by default
            )

            if algorithm == str("plain"):
                """
                If algorithm is text/plain don't do anything 🤷‍♂️
                """
                if (
                    environ["REQUEST_URI"]
                    not in self.STRIP_WHITESPACE_MINIFY_IGNORED_PATHS
                ):
                    headers.append(
                        (
                            "Content-Encoding",
                            "text/plain; charset:utf-8",
                        )
                    )

            elif algorithm != str("plain") and algorithm in accepted_encodings:
                """
                Developer has chosen an algorithm that's not accepted by the browser.
                    So do as the developer says 😄
                """
                if (
                    environ["REQUEST_URI"]
                    not in self.STRIP_WHITESPACE_MINIFY_IGNORED_PATHS
                ):
                    headers.append(
                        (
                            "Content-Encoding",
                            str(self.STRIP_WHITESPACE_COMPRESSION_ALGORITHM),
                        )
                    )
            elif algorithm != str("plain") and algorithm not in accepted_encodings:
                """
                Developer has chosen an algorithm that's not accepted by the browser. 🤦‍♂️
                    So raise an error and explain the error.
                """

                raise ValueError(
                    f"""
                    Error in 'strip_whitespace.middlewares.functions.add_headers'

                        Accepted HTTP ENCODING = { accepted_encodings }

                            Please switch { algorithm } to any of these : { accepted_encodings } in settings.py
                """
                )

            else:
                # Something crazy is going on here. 😱 ( There might be ghosts lurking around here 👀 )

                raise ValueError(
                    f"""
                        'algorithm' in 'strip_whitespace.add_header' must be one of these:
                            |> gzip
                            |> br ( Brotli )
                            |> zstd ( ZStandard )
                            |> plain ( Decompressed HTML )

                        Currently the algorithm is: { algorithm }
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

        if environ["REQUEST_URI"] not in self.STRIP_WHITESPACE_MINIFY_IGNORED_PATHS:
            body = self.__compress__(body)

        return [body]
