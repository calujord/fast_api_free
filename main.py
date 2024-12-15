from fastapi.exceptions import RequestValidationError
from app import MainApi
from controllers.group import Group
from controllers.user import User
import logging
from core.middleware.bad_request import (
    validation_exception_handler,
    validation_unique_handler,
)
from sqlalchemy.exc import PendingRollbackError


# Configurar el registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de la aplicación
logger.info("Creating app instance...")
app = MainApi()

# Agregar controladores
logger.info("Adding controllers...")
app.add_controllers([User, Group])


# Add the middleware class, not an instance
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(PendingRollbackError, validation_unique_handler)

# Construir la aplicación
logger.info("Building app...")
app.build()

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
