import pytest
from utils.security import is_valid_api_key, sanitize_html, sanitize_js_string
from components.fan_companion import get_language_code
from components.incident_command import calculate_priority_score

def test_api_key_validation():
    # Valid key cases
    assert is_valid_api_key("AIzaSyA1234567890123456789012345") is True
    assert is_valid_api_key("AIzaSyB123456789012345678901234567") is True
    
    # Invalid key cases
    assert is_valid_api_key(None) is False
    assert is_valid_api_key("") is False
    assert is_valid_api_key("AIzaSyShort") is False  # Too short
    assert is_valid_api_key("InvalidPrefix12345678901234567890") is False  # Bad prefix
    assert is_valid_api_key(12345678901234567890123456789012) is False  # Non-string

def test_html_sanitization():
    assert sanitize_html("hello") == "hello"
    assert sanitize_html("<div>test</div>") == "&lt;div&gt;test&lt;/div&gt;"
    assert sanitize_html("john & doe") == "john &amp; doe"
    assert sanitize_html('hello "world"') == "hello &quot;world&quot;"
    assert sanitize_html(None) == ""

def test_js_string_sanitization():
    assert sanitize_js_string("hello") == "hello"
    assert sanitize_js_string('hello "world"') == 'hello \\"world\\"'
    assert sanitize_js_string("hello 'world'") == "hello \\'world\\'"
    assert sanitize_js_string("hello\nworld") == "hello world"
    assert sanitize_js_string("hello\\world") == "hello\\\\world"
    assert sanitize_js_string(None) == ""

def test_language_code_mapping():
    assert get_language_code("English") == "en-US"
    assert get_language_code("Español") == "es-ES"
    assert get_language_code("Français") == "fr-FR"
    assert get_language_code("Deutsch") == "de-DE"
    assert get_language_code("Português") == "pt-PT"
    assert get_language_code("日本語") == "ja-JP"
    assert get_language_code("UnknownLanguage") == "en-US"  # Fallback

def test_priority_score_calculation():
    # High risk case
    score, label, badge = calculate_priority_score(
        crowd_size_val="Massive (> 1000 fans)",
        severity_val="High (Immediate Escalation Required)",
        location_val="Gates / Entry Plaza",
        time_val="Post-Match (Egress)"
    )
    assert score > 75
    assert "High" in label
    assert badge == "badge-danger"

    # Low risk case
    score_low, label_low, badge_low = calculate_priority_score(
        crowd_size_val="Small (< 50 fans)",
        severity_val="Low (Routine)",
        location_val="Parking Lot / Shuttle Hub",
        time_val="Mid-Match (In-Play)"
    )
    assert score_low < 40
    assert "Low" in label_low
    assert badge_low == "badge-success"
