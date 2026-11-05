from pydantic import BaseModel, ConfigDict, Field, field_validator


class FoodCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    price: int = Field(ge=0)
    category: str = Field(min_length=1)
    is_available: bool = Field(default=True)

    @field_validator("name", "category")
    @classmethod
    def collapse_spaces(cls, value: str) -> str:
        return " ".join(value.split())

    @field_validator("category")
    @classmethod
    def lowercase_category(cls, value: str) -> str:
        return value.lower()


class FoodRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int
    category: str
    is_available: bool
