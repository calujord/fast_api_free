from app import MainApi
from controllers.group import Group
from controllers.user import User
import logging

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Creating app instance...")
try:
    app = MainApi(setup="instances/config2.yml")
    logger.info("App instance created successfully.")
except Exception as e:
    logger.error(f"Failed to create app instance: {e}")
    raise

try:
    logger.info("Adding controllers...")
    app.add_controllers([User, Group])
    logger.info("Controllers added successfully.")
except Exception as e:
    logger.error(f"Failed to add controllers: {e}")
    raise

try:
    logger.info("Setting up the app...")
    app.setup()
    logger.info("App setup completed successfully.")
except Exception as e:
    logger.error(f"Failed to set up the app: {e}")
    raise

# Enable Swagger documentation
app = MainApi(setup="instances/config2.yml")

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
