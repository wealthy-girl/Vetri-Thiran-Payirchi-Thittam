from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.api.deps import get_current_user

from app.models.recommendation import (
    RecommendationHistory
)

from app.models.schemas import (
    HomeRequest,
    PartyRequest
)

from app.services.recommendation import (
    home,
    party,
    jewelry
)

from app.core.config import settings


router = APIRouter(
    prefix="/api",
    tags=["Recommendations"]
)


def save_recommendation(
    db,
    user,
    planner,
    request_data,
    result
):

    row = RecommendationHistory(

        user_id=user.id,

        planner=planner,

        request_data=request_data,

        response_data=result
    )


    db.add(row)

    db.commit()

    db.refresh(row)

    return result


@router.post("/generate-home")
def generate_home(

    request: HomeRequest,

    user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    result = home(request)


    return save_recommendation(

        db,

        user,

        "home",

        request.model_dump(),

        result
    )


@router.post("/generate-party")
def generate_party(

    request: PartyRequest,

    user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    result = party(request)


    return save_recommendation(

        db,

        user,

        "party",

        request.model_dump(),

        result
    )


@router.post("/generate-jewelry")
async def generate_jewelry(

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form("modern"),

    image: UploadFile | None = File(None),

    user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be positive"
        )


    image_bytes = None

    mime_type = "image/jpeg"


    if image:

        allowed_types = {

            "image/jpeg",

            "image/png",

            "image/webp"
        }


        if image.content_type not in allowed_types:

            raise HTTPException(

                status_code=400,

                detail=
                    "Only JPEG, PNG and WebP "
                    "images are supported"
            )


        image_bytes = await image.read()


        max_bytes = (
            settings.max_image_mb
            * 1024
            * 1024
        )


        if len(image_bytes) > max_bytes:

            raise HTTPException(

                status_code=413,

                detail="Image is too large"
            )


        mime_type = image.content_type


    result = jewelry(

        budget,

        occasion,

        style,

        image_bytes,

        mime_type
    )


    request_data = {

        "budget": budget,

        "occasion": occasion,

        "style": style
    }


    return save_recommendation(

        db,

        user,

        "jewelry",

        request_data,

        result
    )


@router.get("/history")
def history(

    user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    rows = (

        db.query(
            RecommendationHistory
        )

        .filter(
            RecommendationHistory.user_id
            == user.id
        )

        .order_by(
            RecommendationHistory.created_at.desc()
        )

        .all()
    )


    return [

        {

            "id": row.id,

            "planner": row.planner,

            "created_at":
                row.created_at,

            "request":
                row.request_data,

            "response":
                row.response_data
        }

        for row in rows
    ]


@router.get(
    "/recommendations-details/{item_id}"
)
def recommendation_details(

    item_id: int,

    user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    row = (

        db.query(
            RecommendationHistory
        )

        .filter(

            RecommendationHistory.id
            == item_id,

            RecommendationHistory.user_id
            == user.id

        )

        .first()
    )


    if not row:

        raise HTTPException(

            status_code=404,

            detail="Recommendation not found"
        )


    return {

        "id": row.id,

        "planner": row.planner,

        "created_at":
            row.created_at,

        "request":
            row.request_data,

        "response":
            row.response_data
    }