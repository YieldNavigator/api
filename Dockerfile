FROM python:3.11-slim
LABEL authors="JMHong"

WORKDIR /src

# pyproject.toml 및 poetry.lock 파일 복사
COPY pyproject.toml poetry.lock ./

# Poetry 설치 및 패키지 설치
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi


# timezone 설정
ENV TZ=Asia/Seoul

# 볼륨 설정
VOLUME ["~/yieldNavigator/api/yieldNavigator:/src"]

# 컨테이너 시작 시 uvicorn 실행
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
