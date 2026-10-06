from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
    is_active: bool = True
    street: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    tags: list[str] = []


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ada Lovelace",
                    "email": "ada@example.com",
                    "age": 28,
                    "is_active": True,
                    "street": "123 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zip_code": "12345",
                    "tags": ["python", "developer"]
                }
            ]
        }
    }