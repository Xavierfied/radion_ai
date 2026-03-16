import google.generativeai as genai
import base64
import os
from prompts.report_template import DENTAL_ANALYSIS_PROMPT
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use gemini-2.0-flash — free tier, fast, good vision capability
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=DENTAL_ANALYSIS_PROMPT,
)


def get_media_type(file_name: str) -> str:
    """Determine MIME type from file extension."""
    extension = file_name.lower().split(".")[-1]
    media_types = {
        "jpg":  "image/jpeg",
        "jpeg": "image/jpeg",
        "png":  "image/png",
        "gif":  "image/gif",
        "webp": "image/webp",
    }
    return media_types.get(extension, "image/jpeg")


def analyze_xray_g(image_bytes: bytes, file_name: str, patient_id: str, notes: str = "") -> dict:
    """
    Takes an X-ray image and returns a structured analysis report using Gemini.

    Args:
        image_bytes:  Raw bytes of the uploaded image file
        file_name:    Original file name (used to detect media type)
        patient_id:   Patient identifier string (no real names)
        notes:        Any additional clinical notes from the dentist

    Returns:
        dict with keys:
            'success':       bool
            'report':        str (the full structured report)
            'input_tokens':  int
            'output_tokens': int
            'error':         str (only present if success is False)
    """
    try:
        media_type = get_media_type(file_name)

        # Build image part for Gemini
        image_part = {
            "mime_type": media_type,
            "data": image_bytes,
        }

        # Build the text prompt
        user_prompt = (
            f"Please analyze this dental panoramic X-ray for Patient ID: {patient_id}.\n"
            f"Additional clinical notes: {notes if notes else 'None provided.'}\n\n"
            f"Produce the full structured OPG analysis report as instructed."
        )

        # Call Gemini
        response = model.generate_content(
            [image_part, user_prompt],
            generation_config=genai.GenerationConfig(
                max_output_tokens=2000,
                temperature=0.2,  # Low temperature = more consistent, structured output
            ),
        )

        report_text = response.text

        # Gemini returns token usage in usage_metadata
        input_tokens  = getattr(response.usage_metadata, "prompt_token_count",  0)
        output_tokens = getattr(response.usage_metadata, "candidates_token_count", 0)

        return {
            "success":       True,
            "report":        report_text,
            "input_tokens":  input_tokens,
            "output_tokens": output_tokens,
        }

    except Exception as e:
        error_msg = str(e)

        # Give helpful messages for common errors
        if "API_KEY_INVALID" in error_msg or "API key" in error_msg.lower():
            return {
                "success": False,
                "error": "Invalid Gemini API key. Check your GEMINI_API_KEY in the .env file.",
            }
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return {
                "success": False,
                "error": "Free tier rate limit hit. Wait a minute and try again. "
                         "(Free limit: 1,500 requests/day, 15 requests/minute)",
            }
        elif "image" in error_msg.lower() or "vision" in error_msg.lower():
            return {
                "success": False,
                "error": "Image could not be processed. Make sure it is a valid JPEG or PNG dental X-ray.",
            }
        else:
            return {
                "success": False,
                "error": f"Unexpected error: {error_msg}",
            }