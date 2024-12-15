# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Type
from fastapi import FastAPI, Request, Response
from core.database_schema import ConfigSchema
from core.middleware.bad_request import (
    ExceptionMiddleware,
    validation_exception_handler,
    validation_unique_handler,
)
from infrastructure.database.settings import BaseModelEntity

from core.controller import Controller
import yaml
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import PendingRollbackError


class MainApi(FastAPI):
    controllers: list[Type[Controller]] = []

    def __init__(self, setup: str, *args, **kwargs):
        # read config.yml
        with open(setup, "r") as config_file:
            config = yaml.safe_load(config_file)

            settings = ConfigSchema(**config)

            self.docs_url = "/docs"

            self.title = settings.swagger.title
            self.description = settings.swagger.description
            self.version = settings.swagger.version
            self.controllers = []
            self.engine = create_engine(
                settings.database.connection_string,
                connect_args={"check_same_thread": False},
            )
            self.session_local = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            declarative_base()
            BaseModelEntity.metadata.create_all(bind=self.engine)
            super().__init__(*args, **kwargs)

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
        async def db_session_middleware(
            request: Request,
            call_next,
        ) -> Response:
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

    def setup(self) -> None:
        self.setup_routes()
        self.setup_middleware()
