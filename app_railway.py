import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

# --- MOCK CHATBOT (không cần Ollama) ---
# Knowledge base cho chatbot
KNOWLEDGE_BASE = {
    "giờ mở cửa": "Quán mở cửa từ 7:00 sáng đến 22:00 tối hàng ngày, kể cả cuối tuần.",
    "địa chỉ": "Cà Phê Bụi tọa lạc tại 123 Đường ABC, Quận XYZ, TP.HCM.",
    "wifi": "Quán có WiFi miễn phí với tốc độ cao, password: CAFEBUI2024",
    "giá": "Giá dao động từ 20.000đ - 50.000đ. Cà phê phin 25k, Latte 45k, Trà sữa 35k.",
    "menu": "Chúng tôi có: Cà phê (Phin, Sữa đá, Latte, Cappuccino), Trà (Trà sữa, Đào cam sả, Matcha), Bánh (Tiramisu, Croissant, Pancake)",
    "đặt bàn": "Nhóm từ 5 người trở lên vui lòng đặt bàn trước qua hotline: 0123 456 789",
    "combo": "Combo học tập: Cà phê + Bánh ngọt = 55.000đ (tiết kiệm 10k)",
    "giao hàng": "Giao hàng trong bán kính 3km, phí ship 15.000đ, thời gian 30-45 phút",
    "thanh toán": "Nhận tiền mặt, chuyển khoản, Momo, Zalopay"
}

def get_mock_response(question: str) -> str:
    """Tìm câu trả lời phù hợp từ knowledge base"""
    question_lower = question.lower()
    
    # Tìm keyword match
    for keyword, response in KNOWLEDGE_BASE.items():
        if keyword in question_lower:
            return response
    
    # Câu trả lời mặc định
    default_responses = [
        "Xin chào! Cà Phê Bụi chuyên cung cấp cà phê chất lượng cao và bánh ngọt tươi mỗi ngày. Bạn muốn biết thông tin gì?",
        "Quán mở cửa 7h-22h hàng ngày. Menu đa dạng với giá từ 20-50k. Bạn cần hỗ trợ gì thêm không?",
        "Chúng tôi có WiFi miễn phí, không gian yên tĩnh phù hợp làm việc và học tập. Hãy hỏi cụ thể về menu, giá cả, hoặc dịch vụ nhé!"
    ]
    
    # Random response
    import random
    return random.choice(default_responses)

# --- 3. KHỞI TẠO ỨNG DỤNG WEB (FastAPI) ---
app = FastAPI(title="Cà Phê Bụi - AI Chatbot")

# CORS - CHO PHÉP VERCEL FRONTEND
origins = [
    "*",  # Allow all for development
    "https://cafe-ad56fybaw-phamkhanhs-projects-c2663e55.vercel.app",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Cà Phê Bụi API v1.0",
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "health": "/api/health"
        }
    }

@app.post("/chat")
def chat_with_bot(query: Query):
    """API endpoint để chat với AI bot (MOCK version)"""
    try:
        # Sử dụng mock response
        response = get_mock_response(query.text)
        return {"response": response}
    except Exception as e:
        print(f"Lỗi: {e}") 
        return {"error": str(e)}

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "OK", 
        "message": "Server đang hoạt động tốt!",
        "version": "1.0.0-mock"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
