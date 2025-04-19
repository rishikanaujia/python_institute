from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging
from typing import Optional
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Set up templates
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)


# Define routes for each page
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the homepage."""
    logger.info("Rendering homepage")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "page_title": f"{settings.APP_NAME} - {settings.APP_DESCRIPTION}",
            "page_description": "Get certified in Python programming with Python Institute's comprehensive courses and globally recognized certifications. From beginner to professional level Python training and certification."
        }
    )


@router.get("/courses", response_class=HTMLResponse)
async def courses(request: Request):
    """Render the courses page."""
    logger.info("Rendering courses page")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "active_section": "courses",
            "page_title": "Courses - Python Institute",
            "page_description": "Comprehensive Python courses designed to take you from a beginner to a certified professional. Each course builds on the previous one, creating a clear path to Python mastery."
        }
    )


@router.get("/certifications", response_class=HTMLResponse)
async def certifications(request: Request):
    """Render the certifications page."""
    logger.info("Rendering certifications page")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "active_section": "certifications",
            "page_title": "Certifications - Python Institute",
            "page_description": "Our industry-recognized certifications validate your Python skills at different proficiency levels, enhancing your career prospects and professional credibility."
        }
    )


@router.get("/roadmap", response_class=HTMLResponse)
async def roadmap(request: Request):
    """Render the learning roadmap page."""
    logger.info("Rendering roadmap page")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "active_section": "roadmap",
            "page_title": "Learning Roadmap - Python Institute",
            "page_description": "Follow our structured learning path from beginner to professional Python developer. This roadmap will guide you through each stage of your Python journey."
        }
    )


@router.get("/exam-info", response_class=HTMLResponse)
async def exam_info(request: Request):
    """Render the exam information page."""
    logger.info("Rendering exam information page")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "active_section": "exam-info",
            "page_title": "Exam Information - Python Institute",
            "page_description": "Everything you need to know about our Python certification exams, from preparation to test-taking strategies."
        }
    )


@router.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    """Render the FAQ page."""
    logger.info("Rendering FAQ page")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "active_section": "faq",
            "page_title": "FAQ - Python Institute",
            "page_description": "Find answers to common questions about Python Institute certifications and courses."
        }
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Render the contact page."""
    logger.info("Rendering contact page")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "active_section": "contact",
            "page_title": "Contact Us - Python Institute",
            "page_description": "Have questions about our certification program or courses? We're here to help you on your Python journey."
        }
    )


@router.post("/contact", response_class=HTMLResponse)
async def contact_form(
        request: Request,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        subject: str = Form(...),
        message: str = Form(...),
        privacy: bool = Form(...)
):
    """Handle contact form submission."""
    logger.info(f"Contact form submission from {email}")

    # Here you would typically:
    # 1. Validate the data further
    # 2. Send an email
    # 3. Store the contact in a database

    # For now, we'll just log it and show a success message
    try:
        # Simulate processing
        if len(message) < 10:
            raise ValueError("Message is too short")

        # Return success template
        return templates.TemplateResponse(
            "contact_success.html",
            {
                "request": request,
                "settings": settings,
                "name": f"{first_name} {last_name}"
            }
        )
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "settings": settings,
                "active_section": "contact",
                "error": str(e),
                "form_data": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
            }
        )


@router.post("/newsletter-signup", response_class=HTMLResponse)
async def newsletter_signup(
        request: Request,
        email: str = Form(...)
):
    """Handle newsletter signup."""
    logger.info(f"Newsletter signup from {email}")

    # Here you would typically:
    # 1. Validate the email
    # 2. Add the email to your newsletter system
    # 3. Send a confirmation email

    try:
        # Simulate processing
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email address")

        # Return to home page with success message
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "settings": settings,
                "newsletter_success": True,
                "newsletter_email": email
            }
        )
    except Exception as e:
        logger.error(f"Error processing newsletter signup: {str(e)}")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "settings": settings,
                "newsletter_error": str(e),
                "newsletter_email": email
            }
        )


# Error handlers
@router.get("/404", response_class=HTMLResponse)
async def not_found(request: Request):
    """Custom 404 page."""
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "settings": settings,
            "error_code": 404,
            "error_msg": "Page not found",
            "page_title": "404 Not Found - Python Institute"
        },
        status_code=404
    )


@router.get("/500", response_class=HTMLResponse)
async def server_error(request: Request):
    """Custom 500 page."""
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "settings": settings,
            "error_code": 500,
            "error_msg": "Internal server error",
            "page_title": "500 Internal Server Error - Python Institute"
        },
        status_code=500
    )