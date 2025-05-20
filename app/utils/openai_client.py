import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    """Azure OpenAI 클라이언트를 초기화하고 반환합니다."""
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    print(f"Azure OpenAI Config:")
    print(f"- API Version: {api_version}")
    print(f"- Endpoint: {azure_endpoint}")
    print(f"- Deployment: {deployment_name}")
    print(f"- API Key: {'*' * 8 if api_key else 'Not set'}")
    
    if not all([api_key, azure_endpoint, deployment_name]):
        raise ValueError("Azure OpenAI 설정이 완료되지 않았습니다. 환경 변수를 확인해주세요.")
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint
    )
    return client

def get_completion(client, messages, max_completion_tokens=2000):
    """Azure OpenAI를 사용하여 채팅 완성을 생성합니다."""
    try:
        print(f"\nSending request to Azure OpenAI:")
        print(f"Messages: {messages}")
        print(f"Max completion tokens: {max_completion_tokens}")
        
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=messages,
            max_completion_tokens=max_completion_tokens  # max_tokens를 max_completion_tokens로 수정
        )
        
        print(f"\nReceived response from Azure OpenAI:")
        print(f"Response object: {response}")
        print(f"First choice content: {response.choices[0].message.content if response.choices else 'No content'}")
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"\nError in OpenAI API call:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        raise Exception(f"OpenAI API 호출 중 오류 발생: {str(e)}") 