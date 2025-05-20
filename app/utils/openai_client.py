import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    """Azure OpenAI 클라이언트를 초기화하고 반환합니다."""
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    return client

def get_completion(client, messages, max_completion_tokens=800):
    """Azure OpenAI를 사용하여 채팅 완성을 생성합니다."""
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=messages,
            max_completion_tokens=max_completion_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API 호출 중 오류 발생: {str(e)}") 