import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
from pathlib import Path
import jinja2

from app.config import settings
from app.routes import pages

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Mount static files directory
static_dir = Path(settings.STATIC_DIR)
if not static_dir.exists():
    logger.warning(f"Static directory does not exist: {static_dir}")
    static_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created static directory: {static_dir}")

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Set up Jinja2 templates
template_dir = Path(settings.TEMPLATE_DIR)
if not template_dir.exists():
    logger.warning(f"Template directory does not exist: {template_dir}")
    template_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created template directory: {template_dir}")

templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)

# Add custom Jinja2 filters and globals
templates.env.globals["settings"] = settings

# Add custom filters
templates.env.filters["currency"] = lambda value: f"${value:.2f}"

# Add custom Jinja2 extensions
templates.env.add_extension('jinja2.ext.loopcontrols')
templates.env.add_extension('jinja2.ext.do')

try:
    # Add time extensions for things like {% now 'Y' %}
    templates.env.add_extension('jinja2_time.TimeExtension')
except ImportError:
    logger.warning("jinja2_time extension not available. Install with pip install jinja2-time")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware to add process time header and handle exceptions."""
    import time
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        process_time = time.time() - start_time
        if settings.DEBUG:
            # In development, re-raise the exception to see the full traceback
            raise
        else:
            # In production, show a friendly error page
            error_msg = "Internal Server Error"
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error_msg": error_msg},
                status_code=500
            )

# Context processor for all templates
@app.middleware("http")
async def template_context_processor(request: Request, call_next):
    """Add common context variables to all templates."""
    request.state.settings = settings
    request.state.is_debug = settings.DEBUG
    return await call_next(request)

# Include routers
app.include_router(pages.router)

# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app_name": settings.APP_NAME}

if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_NAME} in {'DEBUG' if settings.DEBUG else 'PRODUCTION'} mode")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )