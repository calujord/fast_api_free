import pydantic


class DatabaseSchema(pydantic.BaseModel):
    connection_string: str


class SwaggerSchema(pydantic.BaseModel):
    title: str
    description: str
    docs_url: str = "/docs"
    version: str

    class Config:
        orm_mode = True


class ConfigSchema(pydantic.BaseModel):
    database: DatabaseSchema
    swagger: SwaggerSchema
    port: int

    class Config:
        orm_mode = True
