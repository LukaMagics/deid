# Python 공식 이미지를 기반으로 이미지 생성
FROM python:3.8.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 라이브러리 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . /app/

# 컨테이너 실행 시 실행할 명령 설정
CMD ["python", "fastapi_run.py", "10213"]