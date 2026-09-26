from fastapi import (
    Depends,
    HTTPException,
    Request
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.core.security import decode_token


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):

    token = request.cookies.get(
        "access_token"
    )

    if not token:

        authorization = request.headers.get(
            "Authorization",
            ""
        )

        if authorization.startswith(
            "Bearer "
        ):

            token = authorization[7:]


    payload = (
        decode_token(token)
        if token
        else None
    )


    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )


    subject = payload.get("sub")

    if not subject:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    try:

        user_id = int(subject)

    except ValueError:

        raise HTTPException(
            status_code=401,
            detail="Invalid user token"
        )


    user = db.get(
        User,
        user_id
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    return user