import json
from typing import Optional

from google import genai

from app.core.config import settings


class GeminiService:

    def __init__(self):

        self.client = None

        if settings.gemini_api_key:

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )


    def generate(
        self,
        prompt: str,
        payload: dict,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg"
    ):

        if not self.client:
            return None

        contents = [

            prompt,

            json.dumps(
                payload,
                ensure_ascii=False
            )
        ]

        if image_bytes:

            contents.append({

                "mime_type": mime_type,

                "data": image_bytes
            })


        try:

            response = (
                self.client.models.generate_content(

                    model=settings.gemini_model,

                    contents=contents,

                    config={
                        "response_mime_type":
                            "application/json"
                    }
                )
            )

            text = getattr(
                response,
                "text",
                None
            )

            if not text:
                return None

            return json.loads(text)

        except Exception:

            return None