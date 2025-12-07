🐧 DORI — Multilingual Autonomous Tour Guide Robot
DORI Graduation Project (2024–2025)

다국어 관광 안내 로봇 — 스팟 설명 + RAG 기반 Q&A + 포토스팟 + 웨이크워드

📌 프로젝트 개요

DORI는 경복궁을 따라 이동하며 관광객에게 다국어 설명을 제공하고,
사용자의 질문을 RAG 기반 LLM으로 정확하게 답변해주는
자율주행 관광 안내 로봇입니다.

이번 학기 목표는:

특정 스팟에 대한 설명(TTS)

음성 기반 Q&A(STT + RAG + LLM + TTS)

포토 스팟에서 사진 안내

웨이크워드 "Hey Dori" → 투어 시작

까지의 완전 동작 데모를 구현하는 것입니다.

🧱 프로젝트 전체 구조
dori-project/
├─ app/
│  ├─ (모든 Python 모듈: STT/TTS/RAG/LLM/Orchestrator)
├─ db/
│  ├─ schema.sql / sample_data.sql
├─ credentials/
│  └─ gcp-service-account.json
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md

🔧 기술 스택
분야	사용 기술
언어	Python 3.11
STT/TTS	Google Cloud Speech-to-Text / Text-to-Speech
DB	PostgreSQL + psycopg2
RAG	FAISS + e5-small-v2 + gte-small 임베딩
LLM	로컬(ollama / llama.cpp 등)
배포	Docker / docker-compose
하드웨어	Unitree Go2 + NVIDIA Orin
🎯 핵심 기능
✔ 스팟별 안내 멘트 (다국어 TTS)

영어 원본 스크립트 → 번역 → TTS 재생

✔ RAG 기반 Q&A

Google STT로 사용자 음성 인식

번역 → RAG 검색 → LLM 답변 → 번역 → TTS

“근정전은 언제 지어졌나요?” 같은 질문도 문맥 기반으로 정확하게 답변

✔ 10초 대기 후 자동 다음 스팟 이동

질문이 없으면 “다음 장소로 이동합니다”

✔ 포토 스팟

사진이 잘 나오는 지점에서 사진 촬영 안내

✔ 웨이크워드 “Hey Dori”

추후 Porcupine/Whisper 등 연결 예정

현재는 테스트용 키보드 기반 wakeword 구현

📦 주요 파일 설명 (한–두 줄로 정리)

아래 템플릿은 팀원들이 바로 이해하기 좋도록 주석 스타일 설명으로 정리했어.

📁 app/
dori_main.py

전체 엔트리 포인트. 웨이크워드 감지 → 인사 → 전체 투어 루프 실행.

main_tour_loop.py

스팟 이동/설명/Q&A/포토스팟까지 전체 투어를 순차적으로 실행하는 메인 로직.

multilingual_orchestrator.py

하나의 Q&A 턴을 처리 (STT → 번역 → RAG → LLM → 번역 → TTS).

tts_service.py

Google TTS를 통해 PCM 오디오 생성 후 sounddevice 로 재생.

tts_utils.py

PyAudio 기반 테스트용 TTS 재생 모듈.

stt_service.py

Google Speech-to-Text API로 음성 인식 처리.

wakeword_service.py

“Hey Dori” 웨이크워드 감지 (현재는 콘솔 테스트용).

translation_service.py

번역 모듈 (일반번역 / 질문 → 영어 / 답변 → 사용자 언어). LLM을 사용해서 번역.

llm_client.py

로컬 LLM 호출 래퍼. Ollama/llama.cpp/vLLM 중 하나로 구현 가능.

rag_pipeline.py

RAG 전체 파이프라인: 스크립트 불러오기 / 문맥 생성 / LLM 프롬프트 구성.

faiss_retriever.py

질문 임베딩 → FAISS 검색 → 관련 knowledge_docs 반환.

embedding_client.py

e5 + gte 임베딩 결합하여 RAG 검색 품질을 향상시키는 모듈.

db_utils.py

PostgreSQL CRUD 유틸리티. spots/scripts/knowledge_docs 관리.

tour_route.py

경복궁 스팟 순서 및 스폿 코드 정의.

01_seed_spots.py

tour_route 기반으로 스팟 정보 DB에 삽입.

02_seed_scripts.py

설명 스크립트를 DB에 삽입.

03_seed_knowledge_docs.py

RAG용 knowledge_docs 삽입.

04_build_faiss_index.py

knowledge_docs 임베딩 계산 후 FAISS 인덱스 생성.

📁 db/
schema.sql

PostgreSQL 테이블 구조 정의.

sample_data.sql

기본 languages / place 데이터 삽입.

📁 credentials/
(Google Service Account JSON)

STT/TTS API를 위한 GCP 서비스 계정 키. (절대 깃허브 공개 저장소에 올리면 안 됨)

기타
Dockerfile

dori-app 컨테이너 빌드 스크립트.

docker-compose.yml

PostgreSQL + dori-app을 한 번에 띄우는 서비스 구성.

requirements.txt

Python 의존성 목록.

🚀 실행 방법 (개발)
1. 가상환경 생성
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. 환경설정
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/gcp-service-account.json

3. DB 준비
psql -U postgres -c "CREATE DATABASE dori;"
python app/01_seed_spots.py
python app/02_seed_scripts.py
python app/03_seed_knowledge_docs.py
python app/04_build_faiss_index.py

4. 엔트리 포인트 실행
python app/dori_main.py

🐳 Docker 실행 방법
1. 빌드
docker-compose build

2. 실행
docker-compose up

3. 로그 보기
docker logs -f dori-app

🧭 투어 흐름 요약
"Hey Dori" (웨이크워드)
        ↓
로봇 인사 멘트
        ↓
스팟 #1 이동 → 설명 → Q&A → 사진(옵션)
        ↓
스팟 #2 이동 → 설명 → Q&A
        ↓
...
        ↓
투어 종료 멘트

🙌 팀원들이 알아야 할 핵심 요약

영어가 base 데이터이고, 필요한 언어는 모두 “번역 서비스”로 처리.

STT/TTS는 Google Cloud, Q&A는 로컬 LLM + RAG + 번역.

전체 동작은 dori_main.py → main_tour_loop.py가 담당.

데이터/임베딩/LLM 모두 Docker로 배포 가능.

Unitree Go2 + Orin에서는 docker-compose만 실행하면 됨.
