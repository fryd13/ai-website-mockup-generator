# Website Mockup Generator API

🎨 **AI-powered REST API for generating professional website mockups using GPT-IMAGE-1**

An intelligent FastAPI-based service that generates high-quality website mockups with AI, featuring async email delivery, background task processing, and support for 70+ industry categories.

---

## ✨ Features

- **AI-Powered Generation**
- **Email Delivery**
- **REST API**
---

## 📋 Tech Stack

- **Framework:** FastAPI
- **AI Integration:** OpenAI GPT-IMAGE-1
- **Email:** aiosmtplib (async SMTP)
- **Image Processing:** Pillow
- **Data Validation:** Pydantic v2
- **Server:** Uvicorn
- **Async:** asyncio, httpx

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip
- OpenAI API key
- SMTP server credentials

### Installation

```bash
# Clone the repository
git clone https://github.com/fryd13/ai-website-mockup-generator.git
cd mockup-generator-api

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-image-1
IMAGE_SIZE=1024x1536

# SMTP Configuration
SMTP_SERVER=smtp.server.com
SMTP_PORT=587
SMTP_USERNAME=your_email@domain.com
SMTP_PASSWORD=your_password
SENDER_EMAIL=your_email@domain.com

# API Configuration
API_URL=http://localhost:8000
IMAGE_STORAGE_PATH=./mockups
MAX_RETRIES=3
REQUEST_TIMEOUT=60

# Security
SECRET_KEY=your_secret_key_here_change_in_production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
ALLOWED_IPS=127.0.0.1,::1

# Logging
LOG_DIR=./logs
```
### Running the Server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

Server will start at `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

---

## 📡 API Endpoints

### Generate Mockup

**POST** `/api/v1/generate-mockup`

Create a new website mockup generation task.

**Request Body:**
```json
{
  "keyword": "Modern Coffee Shop E-commerce",
  "industry": "cafe",
  "email": "client@example.com",
  "color_scheme": "modern",
  "additional_details": "Focus on minimalist design with warm colors"
}
```

**Response:**
```json
{
  "status": "processing",
  "message": "Your mockup is being generated. You'll receive an email when it's ready.",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-11-08T10:30:00.000000"
}
```

**Status Codes:**
- `202` – Task created successfully, processing in background
- `400` – Invalid input or email format
- `500` – Server error

---

### Check Task Status

**GET** `/api/v1/task/{task_id}`

Retrieve the current status of a mockup generation task.

**Response:**
```json
{
  "status": "completed",
  "image_url": "http://localhost:8000/mockups/mockup_coffee_20251108_103000.png",
  "email_sent": true,
  "completed_at": "2025-11-08T10:32:45.123456"
}
```

**Possible Statuses:**
- `generating` – AI is creating the mockup
- `sending_email` – Email with mockup is being sent
- `completed` – Mockup generated and email sent
- `failed` – Generation or email sending failed

---

### Health Check

**GET** `/api/v1/health`

Check API availability and version.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-08T10:30:00.000000"
}
```

## 📁 Project Structure

```
mockup-generator-api/
├── main.py                      # FastAPI app entry point
├── config.py                    # Configuration and settings
├── models.py                    # Pydantic models & IndustryEnum
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
│
├── services/
│   ├── openai_service.py       # OpenAI DALL-E integration
│   ├── image_service.py        # Image processing & storage
│   ├── email_service.py        # SMTP email delivery
│   └── email_validator.py      # Email validation
│
├── routes/
│   └── mockup.py               # API endpoints
│
├── mockups/                    # Generated mockup images (created at runtime)
└── logs/                       # Application logs (created at runtime)
```

---

## 🌐 Live Demo

**Test the API live at:** https://pixelduetweb.pl

The live instance features web interface for generating mockups

---

## 👤 Author

**Miłosz Frydrych**

- GitHub: [@fryd13](https://github.com/fryd13)
- Website: [https://pixelduetweb.pl](https://pixelduetweb.pl)
---

**Made with ❤️ by Miłosz Frydrych**
