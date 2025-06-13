# Function to detect file type
def detect_language_from_extension(matched_ext):
    """Returns the file type or programming language based on the file extension."""
    extension_map = {
        # Programming languages
        ".py": "Python", ".java": "Java", ".cpp": "C++", ".c": "C",
        ".js": "JavaScript", ".ts": "TypeScript", ".rb": "Ruby", ".php": "PHP",
        ".go": "Go", ".swift": "Swift", ".kt": "Kotlin", ".rs": "Rust",
        ".lua": "Lua", ".sh": "Shell Script", ".bat": "Batch Script", ".pl": "Perl",
        ".html": "HTML", ".css": "CSS", ".sql": "SQL", ".json": "JSON",
        ".xml": "XML", ".yaml": "YAML", ".toml": "TOML",

        # R language files
        ".r": "R", ".R": "R", ".rmd": "R Markdown", ".rdata": "R Data",
        ".rds": "R Serialized Data", ".rnw": "R with LaTeX (Sweave)",

        # Mathematical and computational languages
        ".m": "MATLAB / Octave", ".mlx": "MATLAB Live Script",
        ".nb": "Mathematica Notebook", ".cdf": "Computable Document Format (Wolfram)",
        ".tex": "LaTeX", ".bib": "BibTeX", ".sty": "LaTeX Style", ".cls": "LaTeX Class",
        ".sage": "SageMath", ".gp": "PARI/GP",

        # Document formats
        ".pdf": "PDF Document", ".doc": "Word Document", ".docx": "Word Document",
        ".odt": "OpenDocument Text", ".txt": "Plain Text", ".rtf": "Rich Text Format",

        # Spreadsheet formats
        ".xls": "Excel Spreadsheet", ".xlsx": "Excel Spreadsheet",
        ".ods": "OpenDocument Spreadsheet", ".csv": "CSV File",

        # Presentation formats
        ".ppt": "PowerPoint Presentation", ".pptx": "PowerPoint Presentation",
        ".odp": "OpenDocument Presentation",

        # Archive formats
        ".zip": "ZIP Archive", ".tar": "TAR Archive", ".gz": "GZIP Archive", ".rar": "RAR Archive",

        # Miscellaneous
        ".md": "Markdown", ".yml": "YAML Configuration"
    }

    return extension_map.get(matched_ext, "Unknown File Type")

# Estimate CHAR_TO_TOKEN_RATIO
def char_to_token_ratio(model_name):
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    sample_text = "This is a sample sentence for estimating token-to-character ratio."
    num_chars = len(sample_text)
    num_tokens = len(tokenizer.encode(sample_text))

    ratio = num_chars / num_tokens
    print(f"Estimated char-to-token ratio: {ratio:.2f}")
    return ratio
