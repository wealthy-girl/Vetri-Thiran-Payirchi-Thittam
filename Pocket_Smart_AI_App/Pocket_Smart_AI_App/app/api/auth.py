from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.models.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserOut
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.api.deps import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=TokenResponse
)
def register(
    data: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    email = str(
        data.email
    ).lower()


    existing = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )


    if existing:

        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )


    user = User(

        name=data.name,

        email=email,

        password_hash=
            hash_password(
                data.password
            )
    )


    db.add(user)

    db.commit()

    db.refresh(user)


    token = create_access_token(
        str(user.id)
    )


    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )


    return {

        "access_token": token,

        "token_type": "bearer",

        "user": user
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    email = str(
        data.email
    ).lower()


    user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )


    if (
        not user
        or not verify_password(
            data.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_access_token(
        str(user.id)
    )


    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )


    return {

        "access_token": token,

        "token_type": "bearer",

        "user": user
    }


@router.post("/logout")
def logout(
    response: Response
):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out successfully"
    }


@router.get(
    "/me",
    response_model=UserOut
)
def me(
    user=Depends(get_current_user)
):

    return user