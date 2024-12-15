# database.py

from fastapi.exceptions import RequestValidationError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Type
from fastapi import FastAPI, Request, Response
from core.middleware.bad_request import (
    ExceptionMiddleware,
    validation_exception_handler,
    validation_unique_handler,
)
from sqlalchemy.exc import PendingRollbackError
from infrastructure.database.settings import BaseModelEntity

from core.controller import Controller


class MainApi(FastAPI):
    controllers: list[Type[Controller]] = []

    def __init__(self, querystring: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = kwargs.get("title", "FastAPI CRUD")
        self.description = kwargs.get("description", "FastAPI CRUD example")
        self.version = kwargs.get("version", "0.1.0")
        self.controllers = []
        self.engine = create_engine(
            querystring, connect_args={"check_same_thread": False}
        )
        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        declarative_base()
        BaseModelEntity.metadata.create_all(bind=self.engine)

    def add_controllers(self, controllers: list[Type[Controller]]):
        for controller in controllers:
            self.controllers.append(controller)

    def setup_routes(self):
        # create all routes dynamically
        print("\033[91mCreating all routes...\033[0m")
        # Run migrations

        for controller_type in self.controllers:
            controller = controller_type()
            controller.session = self.session_local()
            controller._register_routes()

            self.include_router(
                controller.router,
                prefix=controller.prefix,
                tags=getattr(controller, "tags", []),
            )

    def setup_middleware(self):
        @self.middleware("http")
        async def db_session_middleware(request: Request, call_next):
            response = Response("Internal server error", status_code=500)
            try:
                request.state.db = self.session_local()
                response = await call_next(request)
            finally:
                request.state.db.close()
            return response

        self.add_exception_handler(
            RequestValidationError,
            validation_exception_handler,
        )
        self.add_exception_handler(
            PendingRollbackError,
            validation_unique_handler,
        )
        self.add_middleware(ExceptionMiddleware)
