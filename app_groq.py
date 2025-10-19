import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# --- GROQ LLM (FREE & FAST) ---
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Knowledge base
TRI_THUC = """
Cà Phê Bụi - Thông tin quán:

GIỜ MỞ CỬA:
- 7:00 - 22:00 hàng ngày (cả cuối tuần)

ĐỊA CHỈ:
- 123 Đường ABC, Quận XYZ, TP.HCM
- Gần công viên, thuận tiện đậu xe

MENU & GIÁ:
CÀ PHÊ:
- Cà phê phin: 25.000đ
- Cà phê sữa đá: 30.000đ  
- Cappuccino: 45.000đ
- Latte: 45.000đ

TRÀ & ĐỒ UỐNG:
- Trà sữa trân châu: 35.000đ
- Trà đào cam sả: 38.000đ
- Matcha latte: 42.000đ

BÁNH:
- Tiramisu: 45.000đ
- Croissant: 38.000đ
- Pancake: 40.000đ

COMBO ƯU ĐÃI:
- Combo học tập: Cà phê + Bánh = 55.000đ (tiết kiệm 10k)
- Combo cặp đôi: 2 đồ uống + 1 bánh = 95.000đ

DỊCH VỤ:
- WiFi miễn phí (tốc độ cao): Password CAFEBUI2024
- Chỗ đậu xe miễn phí
- Không gian yên tĩnh phù hợp làm việc/học tập
- Giao hàng: Bán kính 3km, phí 15.000đ, 30-45 phút

ĐẶT BÀN:
- Nhóm 5+ người: Gọi trước 0123 456 789
- Đặt online qua website

THANH TOÁN:
- Tiền mặt, Chuyển khoản, Momo, Zalopay
"""

# Initialize Groq client
groq_client = None
if GROQ_AVAILABLE:
    api_key = os.environ.get("GROQ_API_KEY", "")
    if api_key:
        groq_client = Groq(api_key=api_key)

def get_ai_response(question: str) -> str:
    """Get response from Groq LLM or fallback to mock"""
    
    # Try Groq first
    if groq_client:
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"""Bạn là trợ lý AI của quán Cà Phê Bụi. 
Hãy trả lời câu hỏi của khách hàng dựa trên thông tin sau:

{TRI_THUC}

Trả lời ngắn gọn, thân thiện, bằng tiếng Việt. 
Nếu không biết thông tin, hãy lịch sự nói không rõ và đề nghị khách liên hệ trực tiếp."""
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                model="llama3-8b-8192",  # Fast & Free model
                temperature=0.7,
                max_tokens=300,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Groq error: {e}")
    
    # Fallback to mock responses
    return get_mock_response(question)

def get_mock_response(question: str) -> str:
    """Fallback mock responses"""
    question_lower = question.lower()
    
    responses = {
        "giờ": "Quán mở cửa từ 7:00 sáng đến 22:00 tối hàng ngày, kể cả cuối tuần.",
        "mở cửa": "Quán mở cửa từ 7:00 sáng đến 22:00 tối hàng ngày.",
        "địa chỉ": "Cà Phê Bụi tọa lạc tại 123 Đường ABC, Quận XYZ, TP.HCM.",
        "ở đâu": "Quán ở 123 Đường ABC, Quận XYZ, TP.HCM - gần công viên.",
        "wifi": "Có WiFi miễn phí tốc độ cao. Password: CAFEBUI2024",
        "giá": "Giá từ 20-50k. Cà phê phin 25k, Latte 45k, Trà sữa 35k.",
        "menu": "Menu: Cà phê (Phin, Latte, Cappuccino), Trà (Trà sữa, Đào cam sả), Bánh (Tiramisu, Croissant).",
        "combo": "Combo học tập: Cà phê + Bánh = 55k (tiết kiệm 10k)",
        "giao": "Giao hàng trong 3km, phí 15k, thời gian 30-45 phút.",
        "đặt bàn": "Nhóm 5+ người gọi trước: 0123 456 789",
    }
    
    for keyword, response in responses.items():
        if keyword in question_lower:
            return response
    
    return "Xin chào! Cà Phê Bụi mở cửa 7h-22h. Chúng tôi có cà phê, trà, bánh với giá từ 20-50k. WiFi miễn phí. Bạn cần biết thêm gì không?"

# --- FastAPI App ---
app = FastAPI(title="Cà Phê Bụi - AI Chatbot")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

@app.get("/")
async def root():
    return {
        "message": "Cà Phê Bụi API v2.0 - Powered by Groq LLaMA3",
        "status": "running",
        "llm_enabled": groq_client is not None,
        "endpoints": {
            "chat": "/chat",
            "health": "/api/health"
        }
    }

@app.post("/chat")
def chat_with_bot(query: Query):
    """Chat endpoint with Groq LLM"""
    try:
        response = get_ai_response(query.text)
        return {"response": response}
    except Exception as e:
        print(f"Error: {e}")
        return {"response": "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại."}

@app.get("/api/health")
def health_check():
    return {
        "status": "OK",
        "message": "Server đang hoạt động!",
        "version": "2.0.0-groq",
        "llm": "Groq LLaMA3" if groq_client else "Mock"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
