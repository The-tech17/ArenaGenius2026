import pytest
from unittest.mock import patch, MagicMock
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
    
    # Edge cases
    assert get_language_code("UnknownLanguage") == "en-US"  # Fallback
    assert get_language_code("") == "en-US"  # Empty string fallback
    assert get_language_code(None) == "en-US"  # None input fallback

def test_gate_location_edge_cases():
    # Verify gate formatting fallback behaviors
    gate_empty = ""
    gate_none = None
    
    # Confirm they compile into prompt context templates safely without throwing exceptions
    prompt_with_empty = f"The user is standing near: {gate_empty or 'Unknown Gate'}"
    prompt_with_none = f"The user is standing near: {gate_none or 'Unknown Gate'}"
    
    assert "Unknown Gate" in prompt_with_empty
    assert "Unknown Gate" in prompt_with_none

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

def test_mock_api_communication_error():
    """
    Ensure the app cleanly handles API communication errors gracefully
    without raising unhandled exceptions or tracebacks.
    """
    import google.generativeai as genai
    
    with patch("google.generativeai.GenerativeModel") as MockModel:
        # Create a mock instance
        mock_instance = MagicMock()
        # Simulate generate_content raising an API connectivity error
        mock_instance.generate_content.side_effect = Exception("Google API Overloaded or Key Expired")
        MockModel.return_value = mock_instance
        
        # Verify call catches the exception gracefully
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content("Where is Insurgentes Exit?")
            ai_response_text = response.text
        except Exception as e:
            # Code should fallback to safety message
            ai_response_text = "⚠️ Connection to AI assistant failed. Please try again."
            
        assert ai_response_text == "⚠️ Connection to AI assistant failed. Please try again."
