from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.predictor import router as predictor_router
from app.services.modelloader import loadmodel
import uvicorn
from app.logger import get_logger


log = get_logger('Main App')
# Define the lifespan of the application
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # --- Startup: Load the model into a global-style state ---
        log.info("Loading the model")
        app.state.model = loadmodel()
        log.info("model has been loaded")
        yield
        
        # --- Shutdown: Clean up resources if necessary ---
        log.info("Shutting down the application")
        del app.state.model
        log.info("Model state has been deleted")
    except Exception as e:
        log.error(f"Unable to load the model: {e}")

app = FastAPI(
    title="Fraud Detection API",
    description="API for real-time credit card fraud detection",
    version="1.0.0",
    lifespan=lifespan
)

# Include your router
app.include_router(predictor_router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)