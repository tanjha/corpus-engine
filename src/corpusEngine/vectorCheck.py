"""
vectorizable_extensions.py
==========================

A comprehensive catalog of file-type suffixes whose contents can be turned into
human-readable plaintext, and therefore chunked + embedded ("vectorized") for
search / RAG pipelines.

Two practical buckets:

  1. PLAINTEXT_NATIVE  -> the bytes on disk are already text; just decode them.
  2. NEEDS_EXTRACTION  -> binary/container formats that yield text only after a
                          parser/library extracts it (PDF, DOCX, EPUB, ...).

Use `VECTORIZABLE_EXTENSIONS` for a single flat membership check, or the
category dicts below if you want to route each file to the right loader.

All suffixes are lowercase and include the leading dot.

Optional buckets (images via OCR, audio/video via transcription) are provided
separately at the bottom and are NOT included in the defaults, because their
"text" is derived rather than contained in the file.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# 1. PLAINTEXT-NATIVE  (read directly, e.g. open(path, encoding="utf-8"))
# ---------------------------------------------------------------------------

PLAIN_TEXT = {
    ".txt",
    ".text",
    ".log",
    ".nfo",
    ".me",
    ".readme",
    ".asc",
    ".diff",
    ".patch",
}

MARKUP_AND_DOCS_TEXT = {
    ".md",
    ".markdown",
    ".mdown",
    ".mkd",
    ".mdx",
    ".rst",
    ".adoc",
    ".asciidoc",
    ".org",
    ".textile",
    ".creole",
    ".wiki",
    ".tex",
    ".latex",
    ".ltx",
    ".bib",
    ".sty",
    ".cls",
    ".man",
    ".roff",
    ".1",
    ".2",
    ".3",
}

WEB_AND_TEMPLATES = {
    ".html",
    ".htm",
    ".xhtml",
    ".shtml",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".styl",
    ".vue",
    ".svelte",
    ".astro",
    ".jsx",
    ".tsx",
    ".haml",
    ".pug",
    ".jade",
    ".ejs",
    ".erb",
    ".hbs",
    ".handlebars",
    ".mustache",
    ".liquid",
    ".twig",
    ".njk",
    ".j2",
    ".jinja",
    ".jinja2",
}

DATA_AND_CONFIG = {
    ".json",
    ".jsonl",
    ".ndjson",
    ".json5",
    ".jsonc",
    ".geojson",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".config",
    ".properties",
    ".env",
    ".csv",
    ".tsv",
    ".psv",
    ".tab",
    ".xml",
    ".xsd",
    ".xsl",
    ".xslt",
    ".dtd",
    ".rss",
    ".atom",
    ".plist",
    ".svg",
    ".graphql",
    ".gql",
    ".proto",
    ".thrift",
    ".avsc",
    ".prisma",
    ".ron",
    ".hcl",
    ".editorconfig",
    ".gitignore",
    ".gitattributes",
    ".dockerignore",
    ".npmrc",
    ".yarnrc",
}

SOURCE_CODE = {
    # Python
    ".py",
    ".pyw",
    ".pyi",
    ".pyx",
    ".pxd",
    ".rpy",
    # JavaScript / TypeScript
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".mts",
    ".cts",
    ".coffee",
    # C / C++
    ".c",
    ".h",
    ".cpp",
    ".cc",
    ".cxx",
    ".c++",
    ".hpp",
    ".hh",
    ".hxx",
    ".h++",
    ".ino",
    # C# / .NET
    ".cs",
    ".csx",
    ".vb",
    ".fs",
    ".fsx",
    ".fsi",
    # JVM languages
    ".java",
    ".kt",
    ".kts",
    ".scala",
    ".sc",
    ".groovy",
    ".gradle",
    ".clj",
    ".cljs",
    ".cljc",
    ".edn",
    # Go / Rust / Zig / Nim / D / Crystal
    ".go",
    ".rs",
    ".zig",
    ".nim",
    ".nims",
    ".d",
    ".cr",
    # Ruby
    ".rb",
    ".rake",
    ".gemspec",
    ".ru",
    # PHP / Perl
    ".php",
    ".phtml",
    ".php3",
    ".php4",
    ".php5",
    ".pl",
    ".pm",
    ".pod",
    ".t",
    # Swift / Objective-C
    ".swift",
    ".m",
    ".mm",
    # Shell / scripting
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".ksh",
    ".csh",
    ".tcsh",
    ".ps1",
    ".psm1",
    ".psd1",
    ".bat",
    ".cmd",
    # Lua / Tcl / Dart / Julia / R
    ".lua",
    ".tcl",
    ".dart",
    ".jl",
    ".r",
    ".rmd",
    ".rnw",
    # Functional / academic
    ".ex",
    ".exs",
    ".erl",
    ".hrl",
    ".hs",
    ".lhs",
    ".ml",
    ".mli",
    ".elm",
    ".scm",
    ".ss",
    ".lisp",
    ".lsp",
    ".cl",
    ".el",
    ".rkt",
    # Systems / legacy
    ".pas",
    ".pp",
    ".f",
    ".for",
    ".f90",
    ".f95",
    ".f03",
    ".f08",
    ".cob",
    ".cbl",
    ".asm",
    ".s",
    ".vhd",
    ".vhdl",
    ".v",
    ".sv",
    ".vbs",
    # Other
    ".sql",
    ".sol",
    ".gd",
    ".gdscript",
    ".applescript",
    ".scpt",
    ".vala",
    ".hx",
    ".moon",
    ".p",
    ".ada",
    ".adb",
    ".ads",
}

BUILD_AND_INFRA = {
    ".dockerfile",
    ".containerfile",
    ".mk",
    ".cmake",
    ".make",
    ".bazel",
    ".bzl",
    ".buck",
    ".starlark",
    ".star",
    ".tf",
    ".tfvars",
    ".nomad",
    ".jenkinsfile",
    ".cabal",
    ".lock",
}

NOTEBOOKS_AND_LITERATE = {
    ".ipynb",  # JSON container; cell text is readable after parsing
    ".rmd",  # already above, kept for clarity
}

SUBTITLES = {
    ".srt",
    ".vtt",
    ".sub",
    ".ass",
    ".ssa",
    ".sbv",
    ".lrc",
}

EMAIL_TEXT = {
    ".eml",
    ".mbox",
    ".mbx",
}

# Aggregate of everything that is already plaintext on disk
PLAINTEXT_NATIVE = (
    PLAIN_TEXT
    | MARKUP_AND_DOCS_TEXT
    | WEB_AND_TEMPLATES
    | DATA_AND_CONFIG
    | SOURCE_CODE
    | BUILD_AND_INFRA
    | NOTEBOOKS_AND_LITERATE
    | SUBTITLES
    | EMAIL_TEXT
)

# ---------------------------------------------------------------------------
# 2. NEEDS-EXTRACTION  (binary/container; text via a parser library)
#    Suggested library noted per format.
# ---------------------------------------------------------------------------

NEEDS_EXTRACTION = {
    # Documents
    ".pdf",  # pdfplumber / pypdf / PyMuPDF (fitz) / unstructured
    ".doc",  # antiword / textract / LibreOffice
    ".docx",  # python-docx / docx2txt / unstructured
    ".odt",  # odfpy
    ".rtf",  # striprtf
    ".wpd",  # libwpd
    ".epub",  # ebooklib / unstructured
    ".mobi",  # mobi / kindleunpack
    ".azw",
    ".azw3",
    ".fb2",  # ebook-convert (Calibre)
    ".pages",  # Apple Pages (zip container; LibreOffice / textutil)
    # Spreadsheets
    ".xls",  # xlrd
    ".xlsx",
    ".xlsm",  # openpyxl / pandas
    ".ods",  # odfpy / pandas
    ".numbers",  # numbers-parser
    # Presentations
    ".ppt",  # LibreOffice / textract
    ".pptx",  # python-pptx
    ".odp",  # odfpy
    ".key",  # Apple Keynote (LibreOffice)
    # Email containers
    ".msg",  # extract-msg
    ".pst",
    ".ost",  # libpff / readpst
}

# ---------------------------------------------------------------------------
# 3. FLAT SET — use this for a quick "is this file vectorizable?" check
# ---------------------------------------------------------------------------

VECTORIZABLE_EXTENSIONS = frozenset(PLAINTEXT_NATIVE | NEEDS_EXTRACTION)

# Sorted list form, if you prefer a list literal:
VECTORIZABLE_EXTENSIONS_LIST = sorted(VECTORIZABLE_EXTENSIONS)

# ---------------------------------------------------------------------------
# 4. OPTIONAL — derived text, NOT included by default
#    (the file does not *contain* text; text is produced from it)
# ---------------------------------------------------------------------------

OCR_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".bmp",
    ".gif",
    ".webp",
    # via pytesseract / easyocr / unstructured
}

TRANSCRIBABLE_AV_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".ogg",
    ".aac",
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm",
    ".m4v",
    # via whisper / faster-whisper
}

# ---------------------------------------------------------------------------
# 5. Helpers
# ---------------------------------------------------------------------------


def is_vectorizable(path, include_ocr=False, include_av=False) -> bool:
    """Return True if `path`'s suffix can be turned into text."""
    ext = Path(path).suffix.lower()
    if ext in VECTORIZABLE_EXTENSIONS:
        return True
    if include_ocr and ext in OCR_IMAGE_EXTENSIONS:
        return True
    if include_av and ext in TRANSCRIBABLE_AV_EXTENSIONS:
        return True
    # Common extension-less text files (Dockerfile, Makefile, etc.)
    if ext == "" and Path(path).name.lower() in {
        "dockerfile",
        "makefile",
        "rakefile",
        "gemfile",
        "procfile",
        "jenkinsfile",
        "vagrantfile",
        "license",
        "readme",
        "authors",
    }:
        return True
    return False


def needs_extraction_library(path) -> bool:
    """True if the file is binary and requires a parser to read its text."""
    return Path(path).suffix.lower() in NEEDS_EXTRACTION


if __name__ == "__main__":
    # print(f"Plaintext-native suffixes : {len(PLAINTEXT_NATIVE)}")
    # print(f"Needs-extraction suffixes : {len(NEEDS_EXTRACTION)}")
    # print(f"Total vectorizable        : {len(VECTORIZABLE_EXTENSIONS)}")
    # print()
    # print(VECTORIZABLE_EXTENSIONS_LIST)
    pass
