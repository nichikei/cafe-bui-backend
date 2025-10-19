# Cà Phê Bụi - Backend API

FastAPI backend với mock chatbot cho website Cà Phê Bụi.

## Deploy on Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/cafe-bui-backend)

## API Endpoints

- `GET /` - API info
- `POST /chat` - Chatbot endpoint
- `GET /api/health` - Health check

## Environment Variables

No environment variables required for mock version.

## Tech Stack

- FastAPI
- Uvicorn
- Python 3.11

## Local Development

```bash
pip install -r requirements.txt
python app_railway.py
```

Server runs on http://0.0.0.0:8000
