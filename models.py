from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

# Enumeration with predefined values for allowed industries
class IndustryEnum(str, Enum):
	# Technology
	TECH = "technology"
	SAAS = "saas"
	FINTECH = "fintech"
	CYBERSECURITY = "cybersecurity"
	SOFTWARE = "software"
	HARDWARE = "hardware"
	TELECOM = "telecommunications"
	CLOUD = "cloud"
    
    # E-Commerce
	ECOMMERCE = "e-commerce"
	MARKETPLACE = "marketplace"
	DROPSHIPPING = "dropshipping"
	B2B = "b2b"
	GROCERIES = "groceries"
	FASHION = "fashion"
	BEAUTY = "beauty"
	FURNITURE = "furniture"
	AUTOMOTIVE = "automotive"
    
    # Real Estate
	REAL_ESTATE = "real_estate"
	PROPERTY_DEV = "property_development"
	PROPERTY_RENTAL = "property_rental"
	CONSTRUCTION = "construction"
	INTERIOR_DESIGN = "interior_design"
    
	# Gastronomy & Hotels
	RESTAURANT = "restaurant"
	CAFE = "cafe"
	HOTEL = "hotel"
	CATERING = "catering"
	BAR_CLUB = "bar_club"
	BAKERY = "bakery"
    
    # Professional Services
	LAW = "law"
	CONSULTING = "consulting"
	ACCOUNTING = "accounting"
	HR_RECRUITMENT = "hr_recruitment"
	MARKETING_AGENCY = "marketing_agency"
	ADVERTISING = "advertising"
	PR = "pr_communications"
    
    # Education & Training
	EDUCATION = "education"
	UNIVERSITY = "university"
	TRAINING = "training"
	ONLINE_COURSES = "online_courses"
	TUTORING = "tutoring"
	LANGUAGE_SCHOOL = "language_school"

	# Healthcare & Fitness
	HEALTHCARE = "healthcare"
	CLINIC = "clinic"
	PHARMACY = "pharmacy"
	DENTIST = "dentistry"
	PSYCHOLOGIST = "psychology"
	VETERINARY = "veterinary"
	FITNESS = "fitness"
	BEAUTY_SPA = "spa_wellness"
	NUTRITION = "nutrition"

	# Transportation & Logistics
	TRANSPORTATION = "transportation"
	LOGISTICS = "logistics"
	COURIER = "courier"
	TAXI = "taxi"
	MOVING = "moving_services"

	# Real Estate & Home
	REAL_ESTATE_AGENCY = "real_estate_agency"
	HOME_SERVICES = "home_services"
	CLEANING = "cleaning"
	PLUMBING = "plumbing"
	ELECTRICAL = "electrical"
	PAINTING = "painting"
	CARPENTRY = "carpentry"
    
    # Tourism & Travel
	TOURISM = "tourism"
	TRAVEL_AGENCY = "travel_agency"
	HOTEL_BOOKING = "hotel_booking"
	CAR_RENTAL = "car_rental"
	TOUR_OPERATOR = "tour_operator"
    
	# Media & Entertainment
	MEDIA = "media"
	PUBLISHING = "publishing"
	MOVIES = "movies"
	MUSIC = "music"
	GAMING = "gaming"
	STREAMING = "streaming"
	PHOTOGRAPHY = "photography"
	VIDEOGRAPHY = "videography"
    
    # Sports
	SPORTS = "sports"
	GYM = "gym"
	YOGA = "yoga"
	MARTIAL_ARTS = "martial_arts"
	SPORTS_EQUIPMENT = "sports_equipment"
    
    # Retail & Services
	RETAIL = "retail"
	WHOLESALE = "wholesale"
	ANTIQUE_SHOP = "antique_shop"
	BOOKSTORE = "bookstore"
	FLOWER_SHOP = "flower_shop"
	PET_SHOP = "pet_shop"
	JEWELRY = "jewelry"
	ELECTRONICS = "electronics"
    
    # Personal Services
	HAIRDRESSER = "hairdresser"
	BARBER = "barber"
	MANICURE = "manicure_pedicure"
	TATTOO = "tattoo"
	WEDDING_PLANNER = "wedding_planner"
	EVENT_PLANNING = "event_planning"
    
    # Manufacturing & Crafts
	MANUFACTURING = "manufacturing"
	CRAFT = "crafts"
	TEXTILES = "textiles"
	METALWORK = "metalwork"
	CERAMICS = "ceramics"
    
    # Agriculture & Environment
	AGRICULTURE = "agriculture"
	ENVIRONMENTAL = "environmental_protection"
    
    # Finance & Investments
	BANKING = "banking"
	INSURANCE = "insurance"
	INVESTMENT = "investment"
	CRYPTOCURRENCY = "cryptocurrency"
	FOREX = "forex"
    
    # Independent Professionals
	FREELANCER = "freelancer"
	CONSULTANT = "consultant"
	COACH = "coaching"
	
    
    # Uncategorized
	OTHER = "other"
	
class MockupGenerationRequest(BaseModel):
	"""Model for mockup generation request"""
	keyword: str = Field(..., min_length=3, max_length=200, description="Phrase for mockup generation")
	industry: IndustryEnum = Field(..., description="Industry category")
	email: EmailStr = Field(..., description="Client email address")
	color_scheme: Optional[str] = Field(default="modern", description="Color scheme preference")
	additional_details: Optional[str] = Field(default=None, max_length=500, description="Additional information or special requirements")

class MockupGenerationResponse(BaseModel):
	"""Model for mockup generation response"""
	status: str = Field(..., description="Status: 'success', 'processing', or 'error'")
	message: str = Field(..., description="Status message or error description")
	image_url: Optional[str] = Field(None, description="URL to generated mockup image")
	task_id: Optional[str] = Field(None, description="Backend task ID for tracking")
	email_sent: bool = Field(default=False, description="Whether confirmation email was sent to client")
	created_at: Optional[str] = Field(None, description="Timestamp of mockup creation")
