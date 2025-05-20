# Seobi LLM Test

Azure OpenAI를 활용한 LLM 대화를 저장하고 관리하는 Flask 기반 프로젝트입니다.

## 프로젝트 구조

```
seobi-llm-test/
├── app/                   # 애플리케이션 패키지
│   ├── __init__.py        # Flask 앱 팩토리
│   ├── config.py          # 핵심 설정
│   ├── routes/            # API 엔드포인트
│   │   ├── main.py        # 메인 라우트
│   │   └── chat.py        # 채팅 API 라우트
│   ├── models/            # 데이터베이스 모델 (준비됨)
│   └── utils/             # 유틸리티 모듈
│       └── openai_client.py # Azure OpenAI 클라이언트
├── .venv/                  # 가상환경 (uv)
├── .git/                   # Git 저장소
├── .gitignore             # Git 무시 파일 목록
├── .gitmessage.txt        # Git 커밋 메시지 템플릿
├── LICENSE                # 라이선스 파일
├── requirements.txt       # 프로젝트 의존성
├── run.py                # Flask 애플리케이션 실행 스크립트
├── test_chat.py          # API 테스트 스크립트
└── README.md             # 프로젝트 문서
```

## 시작하기

1. Python 가상환경 생성 및 활성화:
```bash
pip install uv
uv venv
```

2. 의존성 설치:
```bash
uv sync
```

3. 환경 변수 설정:
`.env` 파일을 생성하고 다음 내용을 입력합니다:
```env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=your-endpoint-url
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
SECRET_KEY=your-secret-key
ENVIRONMENT=development
```

4. Flask 애플리케이션 실행:
```bash
uv run run.py
```

## API 엔드포인트

### 채팅 API
- `POST /api/chat/completion` - Azure OpenAI와 대화
  ```bash
  # curl 사용
  curl -s -X POST http://localhost:5000/api/chat/completion \
    -H "Content-Type: application/json" \
    -d '{"message": "안녕하세요, 오늘 날씨가 어때요?"}'

  # Python 스크립트 사용
  # 테스트할 때는 Flask 애플리케이션을 실행하고 테스트 스크립트를 실행
  python test_chat.py
  ```

  응답 예시:
  ```json
  {
    "status": "success",
    "message": "안녕하세요, 오늘 날씨가 어때요?",
    "response": "어느 지역의 날씨를 알고 싶으신가요? 거주하시는 도시나 동네명을 알려주시면 오늘 날씨를 안내해 드리겠습니다."
  }
  ```

## 개발 환경

- Python 3.12+
- Flask 3.1.1
- Azure OpenAI API
- uv (패키지 관리자)

## 주요 기능

1. Azure OpenAI API 연동
   - 채팅 완성 API 지원
   - 시스템 프롬프트 설정
   - 대화 기록 지원 (선택적)

2. API 엔드포인트
   - 채팅 완성 API (`/api/chat/completion`)
   - JSON 형식의 요청/응답
   - 에러 처리 및 상태 코드

## 테스트

프로젝트에 포함된 `test_chat.py` 스크립트를 사용하여 API를 테스트할 수 있습니다:

```bash
# 테스트 실행
python3 test_chat.py
```

## 향후 계획

- [ ] 대화 기록 저장 기능
- [ ] 사용자 인증
- [ ] 대화 관리 API
- [ ] 프롬프트 템플릿 관리
- [ ] API 문서화