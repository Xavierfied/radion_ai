import anthropic
import base64
import os
from prompts.report_template import DENTAL_ANALYSIS_PROMPT
from dotenv import load_dotenv

load_dotenv()

# Initialize the Anthropic client once — reused across all calls
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def encode_image(image_bytes: bytes) -> str:
    """Convert raw image bytes to base64 string for the API."""
    return base64.standard_b64encode(image_bytes).decode("utf-8")


def get_media_type(file_name: str) -> str:
    """
    Determine the correct media type from the file extension.
    Claude accepts jpeg, png, gif, webp.
    """
    extension = file_name.lower().split(".")[-1]
    media_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }
    # Default to jpeg if extension not recognized
    return media_types.get(extension, "image/jpeg")


def analyze_xray(image_bytes: bytes, file_name: str, patient_id: str, notes: str = "") -> dict:
    """
    Main function — takes an X-ray image and returns a structured analysis report.

    Args:
        image_bytes:  Raw bytes of the uploaded image file
        file_name:    Original file name (used to detect media type)
        patient_id:   Patient identifier string (no real names)
        notes:        Any additional clinical notes from the dentist

    Returns:
        dict with keys:
            'success': bool
            'report':  str (the full structured report)
            'error':   str (only present if success is False)
    """
    try:
        # Encode the image
        image_data = encode_image(image_bytes)
        media_type = get_media_type(file_name)

        # Build the user message — combines image + any extra context
        user_content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data,
                },
            },
            {
                "type": "text",
                "text": f"Please analyze this dental panoramic X-ray for Patient ID: {patient_id}.\n"
                        f"Additional clinical notes: {notes if notes else 'None provided.'}\n\n"
                        f"Produce the full structured OPG analysis report as instructed.",
            },
        ]

        # Call Claude Sonnet with prompt caching on the system prompt
        # cache_control saves ~90% cost on the system prompt after the first call
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            system=[
                {
                    "type": "text",
                    "text": DENTAL_ANALYSIS_PROMPT,
                    "cache_control": {"type": "ephemeral"},  # Prompt caching
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": user_content,
                }
            ],
        )

        # Extract the text response
        report_text = response.content[0].text

        return {
            "success": True,
            "report": report_text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }

    except anthropic.AuthenticationError:
        return {
            "success": False,
            "error": "Invalid API key. Please check your ANTHROPIC_API_KEY in the .env file.",
        }
    except anthropic.RateLimitError:
        return {
            "success": False,
            "error": "Rate limit hit. Please wait a moment and try again.",
        }
    except anthropic.BadRequestError as e:
        return {
            "success": False,
            "error": f"Image could not be processed. Make sure it is a valid dental X-ray image. Details: {str(e)}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
        }
