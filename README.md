# 원티드 시니어 개발자 대상 과제

## 📝 과제 요구사항
- 아래 기능을 제공하도록 테이블을 설계하고 REST API 서버를 개발
  - 회사명 자동완성
  - 회사 이름으로 회사 검색
  - 태그명으로 회사 검색
  - 회사 태그 정보 추가 및 삭제

## ⏰ 과제 진행시간
2024년 11월 30일 토요일 오전 8시 ~ 2024년 12월 2일 월요일 오전 8시 (48시간)

## 💻 Environments
- OS: 
  - Mac on M1 (local)
- Languages:
  - Python 3.12
- Libraries
  - FastAPI 0.115.5
  - Uvicorn 0.32.1
- Database:
  - PostgreSQL 12.7


# 1. Quick Start

## 1.1 코드 Clone

```shell
$> git clone https://github.com/boring-sinoussi/wanted-senior-developer-test.git
$> cd wanted-senior-developer-test
```

## 1.2 환경변수 설정

```bash
$> cp .env.example .env.local
$> vim .env.local

# == Dotenv Files == #

# - FASTAPI
APP_ENV=local
SECRET_KEY=...

# - DATABASES
DB_URL=postgresql+asyncpg://...
...
```

## 1.3 라이브러리 설치

```bash
$> python3.12 -m venv .venv
$> source .venv/bin/activate
(.venv) $> poetry install
```

## 1.4 Uvicorn 서버 실행

```bash
(.venv) $> uvicorn app.asgi:app
APP_ENV:  local
INFO:     Started server process [32369]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## 1.5 도커 환경으로 서버 실행

```bash
(.venv) $> docker-compose --env-file .env.local up -d
```

# 2. Test

## 2.1 테스트 데이터베이스 실행

```shell
$> docker run -d -p "5432:5432" \
    -e POSTGRES_USER=testuser \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=testdb \
    postgres:12.7
```

## 2.2 테스트 실행

```bash
(.venv) $> pytest
```

## 2.3 커버리지 체크

```shell
(.venv) $> coverage run -m pytest
(.venv) $> coverage report

Name                               Stmts   Miss  Cover
------------------------------------------------------
app/__init__.py                        0      0   100%
...

app/service/tag.py                    31     15    52%
------------------------------------------------------
TOTAL                                299     53    82%
```
