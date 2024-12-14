# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Type
from fastapi import FastAPI
from sqlalchemy import create_engine

from api.controllers.base import Controller
from alembic.config import Config
from alembic import command



class MainApi(FastAPI):
    controllers: list[Type[Controller]] = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controllers = []
        SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Cambia esto a tu URL de base de datos
        engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = declarative_base()
        self.db.metadata.create_all(bind=engine)
        

    def add_controllers(self, controllers: list[Type[Controller]]):
        for controller in controllers:
            self.controllers.append(controller)

    def build(self):
        # create all routes dynamically
        print("\033[91mCreating all routes...\033[0m")
        # Run migrations

        for controller_type in self.controllers:
            controller = controller_type()
            controller.session = self.session_local
            print(f"\033[92mController {self.session_local.__class__} \033[0m")
            print(f"\033[92mController {controller.__class__} \033[0m]")
            # for attr_name in dir(controller):
            #     attr = getattr(controller, attr_name)
            #     if callable(attr) and hasattr(attr, "_path"):
            #         method = getattr(controller.router, attr._methods[0].lower())
            #         method(attr._path)(attr)
            self.include_router(
                controller.router, 
                prefix=controller.prefix, 
                tags=getattr(controller, 'tags', []),
            )
