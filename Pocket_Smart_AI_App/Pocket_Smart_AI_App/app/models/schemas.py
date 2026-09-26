from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=120
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class UserOut(BaseModel):

    id: int
    name: str
    email: EmailStr


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"

    user: UserOut


class HomeRequest(BaseModel):

    budget: float = Field(gt=0)

    rooms: list[str] = Field(
        min_length=1
    )

    style: str = "modern"

    items: dict[str, int] = {}

    priorities: list[str] = []


class PartyRequest(BaseModel):

    budget: float = Field(gt=0)

    guests: int = Field(
        gt=0,
        le=10000
    )

    event_type: str = "birthday"

    venue: str = "home"

    city: str = ""

    priorities: list[str] = []


class RecommendationItem(BaseModel):

    category: str

    name: str

    price: float

    quantity: int = 1

    platform: str

    url: str

    reason: str


class RecommendationResponse(BaseModel):

    planner: str

    budget: float

    allocated: float

    remaining: float

    summary: str

    items: list[RecommendationItem]

    allocations: dict[str, float]

    source: str