from typing import Any, Optional


class VidMindException(Exception):
    """Base exception for all VidMind application errors."""
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.details = details


class VideoNotFoundError(VidMindException):
    """Raised when a requested video cannot be located."""
    pass


class IngestionError(VidMindException):
    """Raised when video download or metadata probing fails."""
    pass


class TranscriptionError(VidMindException):
    """Raised during audio transcription failure."""
    pass


class GroundingError(VidMindException):
    """Raised when evidence verification fails or confidence is too low."""
    pass


class ModelUnavailableError(VidMindException):
    """Raised when an external or local AI model cannot be contacted."""
    pass
