from pydantic import BaseModel

class RecognitionResponse(BaseModel):
    """
    Schema for the response of the /recognize endpoint.
    """
    filename: str
    content_type: str
    plate_text: str
    confidence: float
    valid_format: bool
    latency_ms: int
    engine: str