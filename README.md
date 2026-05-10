# ANPR-evalsys
A prototype for evaluating license plate recognition engines.

## Getting Started
### Prerequisites
- uv
- Python 3.10+

### Install dependencies
```bash
uv sync
``` 

### Run the application
inside /src folder:
```bash
uv run uvicorn app.main:app --reload
```

### Access the API documentation
http://localhost:8000/docs
![alt text](data/readme_img/api_docs.png)
## Architecture
Image -> (Detection) -> Crop -> Preprocessing -> OCR -> Postprocessing -> Result API

## API Endpoints
- `POST /recognize`: Accepts an uploaded image and returns the evaluation results.

Example via OpenAPI docs:
![alt text](data/readme_img/api_ex.png)
## Metrics
- Exact plate accuracy
- Character accuracy
- Latency
- Detection success rate

Current evaluation results on the 10 test images:
![alt text](data/readme_img/benchmark_df.png)
![alt text](data/readme_img/benchmark.png)

## Dataset
- Germany License Plate Dataset: Preview
https://www.kaggle.com/datasets/unidpro/germany-license-plate-dataset?resource=download

## Stack 
- Python
- FastAPI
- OpenCV
- EasyOCR
