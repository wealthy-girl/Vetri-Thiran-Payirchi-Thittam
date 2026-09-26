from app.services.catalog import (
    fallback_home,
    fallback_party,
    fallback_jewelry
)

from app.services.gemini_service import (
    GeminiService
)

from app.services.prompts import (
    HOME_PROMPT,
    PARTY_PROMPT,
    JEWELRY_PROMPT
)


gemini = GeminiService()


def home(req):

    result = gemini.generate(
        HOME_PROMPT,
        req.model_dump()
    )

    if result:
        return result

    return fallback_home(req)


def party(req):

    result = gemini.generate(
        PARTY_PROMPT,
        req.model_dump()
    )

    if result:
        return result

    return fallback_party(req)


def jewelry(
    budget,
    occasion,
    style,
    image_bytes=None,
    mime_type="image/jpeg"
):

    payload = {

        "budget": budget,

        "occasion": occasion,

        "style": style
    }

    result = None

    if image_bytes:

        result = gemini.generate(
            JEWELRY_PROMPT,
            payload,
            image_bytes,
            mime_type
        )

    if result:
        return result

    return fallback_jewelry(
        budget,
        occasion,
        style
    )