import requests
import json

def test_chat():
    url = "http://localhost:5000/api/chat/completion"
    headers = {"Content-Type": "application/json"}
    data = {"message": "안녕하세요, 오늘 날씨가 어때요?"}
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    print("\n=== 대화 내용 ===")
    print(f"질문: {result['message']}")
    print(f"답변: {result['response']}")
    print("===============\n")

if __name__ == "__main__":
    test_chat() 