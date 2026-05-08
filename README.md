# ANPR-evalsys
A prototype for evaluating license plate recognition engines.

## Architecture
Image -> Detection -> Crop -> OCR -> Postprocessing -> Result API

## API Endpoints
- `POST /recognize`: Accepts an uploaded image and returns the evaluation results.

## Metrics
- Exact plate accuracy
- Character accuracy
- Latency
- Detection success rate

## Stack 
- Python
- FastAPI
- OpenCV
- EasyOCR
- YOLO
- PostgreSQL
- Docker
- pytest