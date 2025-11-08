import base64
import os
from pathlib import Path
from datetime import datetime
import logging
from PIL import Image
from io import BytesIO
from config import settings

logger = logging.getLogger(__name__)

# Service for processing, validating, and storing base64-encoded images
class ImageService:

    # Initialize image service and create storage directory if needed
    def __init__(self):
        self.storage_path = Path(settings.IMAGE_STORAGE_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    # Decode base64 image, save to disk with timestamped filename
    def save_image(self, image_b64: str, keyword: str, format: str = "png"):
    
        # Decode base64 to image bytes
        image_data = base64.b64decode(image_b64)

        # Open image from bytes
        image = Image.open(BytesIO(image_data))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Sanitize keyword - keep only alphanumeric and underscores
        safe_keyword = "".join(c for c in keyword if c.isalnum() or c == "_")[:30]
        filename = f"mockup_{safe_keyword}_{timestamp}.{format}"

        file_path = self.storage_path / filename

        try:
            # Save image with high quality
            if format.lower() == "png":
                image.save(file_path,"PNG", quality=99)
            else:
                image.save(file_path, "JPG", quality=99)

            file_url = f"{settings.API_URL}/mockups/{filename}"

            logger.info(f"Image saved: {file_path}")
            return str(file_path), file_url

        except Exception as e:
            logger.error(f"Failed save: {str(e)}")
            raise

    # Validate base64 image data - check if it's decodable and has valid dimensions.
    def validate_image_data(self,image_b64: str):
        try:
            image_data = base64.b64decode(image_b64)
            image = Image.open(BytesIO(image_data))
                               
            return image.size[0] > 0 and image.size[1] > 0

        except Exception as e:
            return False

image_service = ImageService()