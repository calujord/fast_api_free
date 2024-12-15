from app import MainApi
from controllers.group import Group
from controllers.user import User
import logging

# Configurar el registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de la aplicación
logger.info("Creating app instance...")
app = MainApi()

# Agregar controladores
logger.info("Adding controllers...")
app.add_controllers([User, Group])

# Construir la aplicación
logger.info("Building app...")
app.build()

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
