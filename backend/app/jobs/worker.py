from app.core.config import get_settings


def run_worker() -> None:
    settings = get_settings()
    print(f"Starting worker in environment {settings.environment}")
