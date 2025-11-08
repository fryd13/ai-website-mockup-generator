from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
import uuid
from models import MockupGenerationRequest, MockupGenerationResponse
from services.openai_service import openai_service
from services.email_service import email_service
from services.image_service import image_service
from services.email_validator import validate_email

# logger init
logger = logging.getLogger(__name__)
#router init
router = APIRouter(prefix="/api/v1", tags=["mockups"])

# In-memory storage for task states
tasks_store = {}

# Mockup generation endpoint
@router.post("/generate-mockup", response_model=MockupGenerationResponse)
async def generate_mockup(
    request: MockupGenerationRequest,
    background_tasks: BackgroundTasks
):
    if not validate_email(request.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    task_id = str(uuid.uuid4())
    
    try:
        # Walidacja podstawowa
        if not request.keyword.strip():
            raise HTTPException(
                status_code=400,
                detail="Keyword cannot be empty"
            )
        
        # Dodaj task do background
        background_tasks.add_task(
            process_mockup_generation,
            task_id,
            request
        )
        
        return MockupGenerationResponse(
            status="processing",
            message="Your mockup is being generated. You'll receive an email when it's ready.",
            task_id=task_id,
            created_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in generate_mockup: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Async Background processing
async def process_mockup_generation(
    task_id: str,
    request: MockupGenerationRequest
):
    
    try:
        tasks_store[task_id] = {"status": "generating"}
        
        # Generate mockup
        image_b64, revised_prompt = await openai_service.generate_mockup(
            keyword=request.keyword,
            industry=request.industry.value,
            additional_details=request.additional_details
        )
        
        # Image validation
        if not image_service.validate_image_data(image_b64):
            raise Exception("Generated image validation failed")
        
        # Save file
        file_path, file_url = image_service.save_image(
            image_b64,
            request.keyword,
            format="png"
        )
        
        # Decode base64 for email attachment
        import base64
        image_bytes = base64.b64decode(image_b64)
        
        # Update task status to completed
        tasks_store[task_id] = {"status": "sending_email"}
        email_sent = await email_service.send_mockup_email(
            recipient_email=request.email,
            image_data=image_bytes,
            image_filename="mockup.png",
            keyword=request.keyword,
            industry=request.industry.value
        )
        
        # Update task status to completed
        tasks_store[task_id] = {
            "status": "completed",
            "image_url": file_url,
            "email_sent": email_sent,
            "completed_at": datetime.now().isoformat()
        }
        
        logger.info(f"Task {task_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {str(e)}")
        tasks_store[task_id] = {
            "status": "failed",
            "error": str(e)
        }

# Task status endpoint
@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    
    if task_id not in tasks_store:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    return tasks_store[task_id]

# Health check endpoint for monitoring API availability.
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }