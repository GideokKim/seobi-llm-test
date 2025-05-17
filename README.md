# Seobi LLM Test

Azure OpenAI를 활용한 LLM 대화를 저장하고 관리하는 Flask 기반 프로젝트입니다.

## 프로젝트 구조

```
seobi-llm-test/
├── app/
│   ├── api/            # API 엔드포인트 (conversations.py, chat.py)
│   ├── core/           # 핵심 설정 (config.py)
│   ├── db/             # 데이터베이스 모델 및 설정
│   ├── schemas/        # 데이터 모델
│   └── main.py         # Flask 애플리케이션 진입점
├── migrations/         # 데이터베이스 마이그레이션 파일
├── alembic/           # Alembic 설정
├── .env               # 환경 변수 (git에 포함되지 않음)
├── requirements.txt   # 프로젝트 의존성
└── README.md         # 프로젝트 문서
```

## 시작하기

1. Python 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
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

4. 데이터베이스 초기화:
```bash
# 기존 마이그레이션 삭제 (필요한 경우)
rm -rf migrations/
rm -f app/app.db

# 마이그레이션 초기화
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. 서버 실행:
```bash
# 환경 변수 설정
export PYTHONPATH=$PYTHONPATH:$(pwd)
export FLASK_APP=app.main

# 서버 실행
flask run --debug
```

## API 엔드포인트

### 기본 엔드포인트
- `GET /` - 환영 메시지
- `GET /health` - 헬스 체크
- `GET /env-check` - 환경 설정 확인

### 대화 관리
- `GET /api/conversations` - 대화 목록 조회
- `GET /api/conversations/<id>` - 특정 대화 조회
- `POST /api/conversations` - 새 대화 생성
- `DELETE /api/conversations/<id>` - 대화 삭제

### 채팅
- `POST /api/chat/<id>/completion` - Azure OpenAI와 대화

## API 테스트

### 새 대화 생성
```bash
curl -X POST http://localhost:5000/api/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "테스트 대화"}'
```

### LLM과 대화
```bash
curl -X POST http://localhost:5000/api/chat/1/completion \
  -H "Content-Type: application/json" \
  -d '{"message": "안녕하세요, 오늘 날씨가 어때요?"}'
```

### 대화 내용 확인
```bash
curl http://localhost:5000/api/conversations/1
```

## 환경 변수

프로젝트를 실행하기 위해 다음 환경 변수들을 설정해야 합니다:

- `AZURE_OPENAI_API_KEY`: Azure OpenAI API 키
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI 엔드포인트 URL
- `AZURE_OPENAI_API_VERSION`: API 버전 (기본값: 2024-02-15-preview)
- `AZURE_OPENAI_DEPLOYMENT_NAME`: 배포된 모델 이름
- `SECRET_KEY`: 애플리케이션 시크릿 키
- `ENVIRONMENT`: 실행 환경 (development/production)

## 개발 환경

- Python 3.12+
- Flask 3.0.0+
- SQLAlchemy 2.0.0+
- Azure OpenAI API
- SQLite (개발 환경)