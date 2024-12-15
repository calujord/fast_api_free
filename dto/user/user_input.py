import pydantic


class UserInput(pydantic.BaseModel):
    name: str = pydantic.Field(title="User name")
    email: str = pydantic.Field(
        title="User email",
        pattern=r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$",
        min_length=6,
        max_length=50,
        examples=["info@info.com"],
    )
    password: str = pydantic.Field(title="User password")
    group_id: int = pydantic.Field(title="User group id")
