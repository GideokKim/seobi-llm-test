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
│   │   ├── message.py     # 메시지 API 라우트
│   │   ├── session.py     # 세션 API 라우트
│   │   └── user.py        # 사용자 API 라우트
│   ├── models/            # 데이터베이스 모델
│   │   ├── message.py     # 메시지 모델
│   │   ├── session.py     # 세션 모델
│   │   └── user.py        # 사용자 모델
│   └── utils/             # 유틸리티 모듈
│       └── openai_client.py # Azure OpenAI 클라이언트
├── .venv/                  # 가상환경 (uv)
├── .git/                   # Git 저장소
├── .gitignore             # Git 무시 파일 목록
├── .gitmessage.txt        # Git 커밋 메시지 템플릿
├── LICENSE                # 라이선스 파일
├── requirements.txt       # 프로젝트 의존성
├── run.py                # Flask 애플리케이션 실행 스크립트
├── docker-compose.yml    # Docker Compose 설정
├── Dockerfile            # Flask 애플리케이션 Dockerfile
├── Dockerfile.postgres   # PostgreSQL Dockerfile
└── README.md             # 프로젝트 문서
```

## 시작하기

### 로컬 환경에서 실행

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
# Azure OpenAI 설정
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=your-endpoint-url
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name

# Flask 설정
SECRET_KEY=your-secret-key
ENVIRONMENT=development

# 데이터베이스 설정
DATABASE_URL=
POSTGRES_DB=seobi
POSTGRES_USER=
POSTGRES_PASSWORD=
```

4. Flask 애플리케이션 실행:
```bash
uv run run.py
```

### Docker로 실행

1. Docker와 Docker Compose 설치 (필요한 경우)

2. 환경 변수 설정:
`.env` 파일을 위와 같이 설정합니다.

3. Docker 컨테이너 실행:
```bash
docker compose up -d
```

4. 로그 확인:
```bash
docker compose logs -f web
```

## API 엔드포인트

### 사용자 API
- `POST /api/users` - 새 사용자 생성
  ```bash
  curl -X POST http://localhost:5000/api/users \
    -H "Content-Type: application/json" \
    -d '{"username": "test_user", "email": "test@example.com"}'
  ```
- `GET /api/users/<user_id>` - 사용자 정보 조회
- `PUT /api/users/<user_id>` - 사용자 정보 수정
- `DELETE /api/users/<user_id>` - 사용자 삭제

### 세션 API
- `POST /api/sessions` - 새 대화 세션 생성
  ```bash
  curl -X POST http://localhost:5000/api/sessions \
    -H "Content-Type: application/json" \
    -d '{"user_id": "user-uuid", "content": "첫 메시지 내용"}'
  ```
- `GET /api/sessions` - 모든 세션 목록 조회
- `GET /api/sessions/<session_id>` - 특정 세션 정보 조회
- `POST /api/sessions/<session_id>/finish` - 세션 종료
- `DELETE /api/sessions/<session_id>` - 세션 삭제

### 메시지 API
- `POST /api/messages/session/<session_id>` - 새 메시지 전송 및 AI 응답 받기
  ```bash
  curl -X POST http://localhost:5000/api/messages/session/session-uuid \
    -H "Content-Type: application/json" \
    -d '{"user_id": "user-uuid", "content": "메시지 내용"}'
  ```
- `GET /api/messages` - 모든 메시지 조회
- `GET /api/messages/<message_id>` - 특정 메시지 조회
- `DELETE /api/messages/<message_id>` - 메시지 삭제

## 개발 환경

- Python 3.12+
- Flask 3.1.1
- PostgreSQL 16+ (pgvector 확장 포함)
- Azure OpenAI API
- Docker & Docker Compose
- uv (패키지 관리자)

## 주요 기능

1. 사용자 관리
   - 사용자 생성 및 관리
   - 사용자별 세션 관리

2. 세션 관리
   - 대화 세션 생성 및 종료
   - 세션별 메시지 관리
   - 세션 제목 자동 생성

3. 메시지 관리
   - Azure OpenAI API를 통한 대화
   - 메시지 히스토리 저장
   - 벡터 임베딩 지원 (pgvector)

4. 데이터베이스
   - PostgreSQL + pgvector
   - 메시지 벡터 저장 및 검색
   - 세션 및 사용자 데이터 관리

## 테스트

### 로컬 환경에서 테스트
```bash
# Flask 서버 실행
uv run run.py

# 새 터미널에서 curl로 테스트
# 1. 사용자 생성
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "email": "test@example.com"}'

# 2. 세션 생성 (user_id는 위 응답에서 받은 ID 사용)
curl -X POST http://localhost:5000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user-uuid", "content": "안녕하세요"}'

# 3. 메시지 전송 (session_id는 위 응답에서 받은 ID 사용)
curl -X POST http://localhost:5000/api/messages/session/session-uuid \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user-uuid", "content": "파이썬이란 무엇인가요?"}'
```

### Docker 환경에서 테스트
```bash
# Docker 컨테이너 실행
docker compose up -d

# 로그 확인
docker compose logs -f web

# 위의 curl 명령어들을 localhost:5000으로 실행
```

## 향후 계획

- [x] 대화 기록 저장 기능
- [x] 사용자 인증
- [x] 대화 관리 API
- [ ] 프롬프트 템플릿 관리
- [ ] API 문서화