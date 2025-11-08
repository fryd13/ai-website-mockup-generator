import re
import logging

logger = logging.getLogger(__name__)

# Validate email address format using regex pattern.
def validate_email(email: str):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None




