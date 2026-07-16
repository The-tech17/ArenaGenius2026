import html

def is_valid_api_key(key):
    """
    Ensure raw API keys never leak into logs or UI error frames and check format.
    Gemini keys usually start with AIzaSy... and are at least 30 characters long.
    """
    if not key or not isinstance(key, str):
        return False
    return key.startswith("AIzaSy") and len(key) >= 30

def sanitize_html(text):
    """
    Encodes HTML special characters to prevent HTML injection in unsafe_allow_html blocks.
    """
    if not text:
        return ""
    return html.escape(str(text))

def sanitize_js_string(text):
    """
    Escapes a string so it can be safely embedded inside a JavaScript string literal.
    """
    if not text:
        return ""
    # Standard JS string escaping: escape backslashes and double/single quotes, strip newlines
    escaped = str(text).replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'").replace("\n", " ").replace("\r", " ")
    return escaped
