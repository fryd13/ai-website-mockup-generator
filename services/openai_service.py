import openai
import httpx
import logging
import base64
from config import settings
from typing import Optional

logger = logging.getLogger(__name__)

# Service for generating website mockups using OpenAI API
class OpenAIService:

    # Initialize OpenAI service with API credentials and configuration
    def __init__(self):
        
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.api_url = "https://api.openai.com/v1/images/generations"
        self.timeout = settings.REQUEST_TIMEOUT
        
    # Generate mockup image using OpenAI DALL-E.
    def create_prompt(self, keyword: str, industry: str, additional_details: Optional[str] = None):
        prompt = f"""Create a professional website mockup based on:
                    Keyword/Topic: {keyword}
                    Industry: {industry}
                    Details: {additional_details or 'None'}

                    Requirements:
                    - Modern, colorful design
                    - Clear typography
                    - Good contrast and appropriate color palette
                    - Responsive layout
                    - Header, hero section, features, several thematic sections, CTA, contact form, footer
                    - Realistic content
                    - High-quality appearance
                    - Fit within 1024x1536 size, do not crop images

                    CRITICAL REQUIREMENTS FOR TEXT AND TYPOGRAPHY:
                    - All text must be CLEAN, READABLE, and PROFESSIONAL
                    - Use only standard characters
                    - Clear sans-serif typography (Arial, Helvetica, or modern web fonts)

                    Create a professional website mockup."""

        return prompt
    
    async def generate_mockup(self, keyword: str, industry: str, additional_details: Optional[str] = None):
        
        prompt = self.create_prompt(
            keyword, industry, additional_details
        )

        # Prepare OpenAI API request headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Build request payload for image generation
        payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "n": 1,
                    "size": settings.IMAGE_SIZE,
                    #"response_format": "b64_json"
                }
        
        try:
            # Make async request to OpenAI API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
            
            

            data = response.json()
            image_b64 = data["data"][0]["b64_json"]
            revised_prompt = data["data"][0].get("revised_prompt", prompt)
            
            logger.info(f"Mockup generated successfully for: {keyword}")
            return image_b64, revised_prompt
            
        except httpx.HTTPError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate mockup: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in generate_mockup: {str(e)}")
            raise

openai_service = OpenAIService()
