from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerEmailRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    from_: EmailStr = Field(alias="from", max_length=254)
    subject: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=10, max_length=10_000)

    @field_validator("subject", "body")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class EmailResponse(BaseModel):
    success: bool
    summary: str | None = None
    reply: str | None = None
    error: str | None = None
