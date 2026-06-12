from fastapi import FastAPI
from pydantic import BaseModel

from config import TEMP_SCRIPT
from pipeline.orchestrator import Orchestrator
from pipeline.logger import PipelineLogger
from models.model_loader import ModelLoader

from config import MAX_RETRIES

app = FastAPI(
    title="Multi-Agent AI Python Code Generator"
)

orchestrator = Orchestrator()

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    success: bool
    code: str
    stdout: str
    stderr: str
    attempts: int

@app.on_event("startup")
def startup():

    PipelineLogger.initialize()

@app.get("/")
def root():

    return {
        "message":
        "Multi-Agent AI Python Code Generator API"
    }

@app.get("/status")
def status():

    return {
        "model_name":
        ModelLoader.get_model_name(),

        "model_loaded":
        ModelLoader.is_loaded(),

        "runtime":
        ModelLoader.get_runtime(),

        "max_retries":
        MAX_RETRIES
    }

@app.post(
    "/generate",
    response_model=GenerateResponse
)

def generate(
    request: GenerateRequest
):

    result = orchestrator.run(
        request.prompt
    )

    return GenerateResponse(
        success=result["success"],
        code=result["code"],
        stdout=result["stdout"],
        stderr=result["stderr"],
        attempts=result["attempts"]
    )

@app.post("/reset")
def reset():

    PipelineLogger.clear_logs()

    if TEMP_SCRIPT.exists():
        TEMP_SCRIPT.unlink()

    return {
        "message":
        "Pipeline reset successful."
    }