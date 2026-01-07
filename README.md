# 🐧 DORI — 다국어 자율주행 관광 안내 로봇

**DORI (다국어 관광 안내 로봇)** 는 문화유산지, 특히 서울의 경복궁을 방문하는 관광객에게 다국어 안내를 제공하도록 설계된 자율주행 관광 안내 로봇 시스템입니다.

## 📋 프로젝트 개요

DORI는 세 가지 핵심 모듈을 통합합니다:
1. **다국어 Q&A 시스템**: RAG 기반 LLM을 활용한 지능형 질문 답변
2. **사진 촬영 도리**: 자동화된 관광객 사진 촬영 (프레임워크 구현 완료)
3. **자율주행 내비게이션**: 센서 융합 기반 (계획 중)

이 시스템은 **8개 언어** (영어, 한국어, 일본어, 중국어, 프랑스어, 스페인어, 베트남어, 태국어)를 지원하며, RAG(Retrieval-Augmented Generation)를 사용한 맥락 인식 답변과 실시간 음성 대화를 제공합니다.

## ✅ 완료된 기능

### 핵심 인프라
- ✅ **PostgreSQL 데이터베이스**: 계층적 구조 (장소 → 스팟 → 스크립트)
- ✅ **지식 베이스**: RAG용 30개 이상의 지식 문서
- ✅ **FAISS 벡터 인덱스**: 컨텍스트 검색을 위한 고속 의미 검색
- ✅ **듀얼 임베딩 모델**: 향상된 검색을 위한 e5-small-v2 + gte-small

### 다국어 지원
- ✅ **8개 언어**: 영어, 한국어, 일본어, 중국어, 프랑스어, 스페인어, 베트남어, 태국어
- ✅ **실시간 번역**: LLM 기반 번역 파이프라인
- ✅ **번역 캐싱**: 캐시된 번역으로 성능 최적화
- ✅ **언어 자동 감지**: 웨이크워드에서 자동 감지

### 음성 서비스
- ✅ **STT (음성 인식)**: Whisper (오프라인, tiny 모델) 음성 인식
- ✅ **TTS (음성 합성)**: Google Cloud Text-to-Speech 자연스러운 음성 합성
- ✅ **다국어 인식**: 8개 언어 모두 지원

### 웨이크워드 감지
- ✅ **음성 기반 감지**: "Hey Dori" (영어) / "도리야" (한국어)
- ✅ **퍼지 매칭**: Levenshtein 거리를 사용한 발음 변형 처리
- ✅ **언어 자동 감지**: 웨이크워드에서 사용자 언어 결정
- ✅ **쿨다운 메커니즘**: 중복 트리거 방지

### 투어 루프 시스템
- ✅ **완전한 투어 오케스트레이션**: 6개 스팟을 순차적으로 탐색
- ✅ **스팟 소개**: 각 위치에 대한 TTS 내레이션
- ✅ **Q&A 세션**: 10초 타임아웃이 있는 대화형 질문 답변
- ✅ **인라인 웨이크워드 인터럽트**: 사용자가 내레이션 중에 중단 가능
- ✅ **자동 진행**: 질문이 없으면 다음 스팟으로 이동

### RAG 기반 Q&A 시스템
- ✅ **RAG 파이프라인**: 지식 베이스에서 FAISS 기반 의미 검색
- ✅ **LLM 통합**: LM Studio를 통한 로컬 LLM (Llama-3.1-8B-Instruct)
- ✅ **고유명사 정규화**: 궁궐 이름의 잘못된 발음 처리
- ✅ **다중 턴 Q&A**: 후속 질문 지원
- ✅ **"패스" 명령**: 사용자가 질문을 건너뛸 수 있음
- ✅ **RAG 토글**: config 플래그로 RAG 활성화/비활성화 가능

### 포토 스팟 기능
- ✅ **포토 스팟 감지**: 지정된 사진 위치 식별
- ✅ **위치 안내**: 사용자를 최적 위치로 안내
- ✅ **카운트다운 시스템**: 촬영 전 5초 카운트다운
- ⚠️ **카메라 통합**: 프레임워크 준비 완료, 하드웨어 통합 대기 중

## 🏗️ 시스템 아키텍처

### 기술 스택

| 구성 요소 | 기술 |
|-----------|-----------|
| **프로그래밍 언어** | Python 3.11 |
| **데이터베이스** | PostgreSQL + psycopg2 |
| **음성 인식** | Whisper (오프라인, tiny 모델) |
| **음성 합성** | Google Cloud Text-to-Speech |
| **LLM** | 로컬 LLM (LM Studio / Ollama / llama.cpp) |
| **RAG** | FAISS + e5-small-v2 + gte-small 임베딩 |
| **배포** | Docker / docker-compose |
| **하드웨어** | Unitree Go2 사족 보행 로봇 + NVIDIA Orin |

### 데이터 흐름

**Q&A 파이프라인:**
```
사용자 음성 → STT (Whisper) → 언어 감지
    ↓
번역 (사용자 언어 → 영어) → RAG 컨텍스트 검색
    ↓
LLM 답변 생성 → 번역 (영어 → 사용자 언어)
    ↓
TTS (Google Cloud) → 오디오 출력
```

**투어 흐름:**
```
웨이크워드 감지 → 언어 자동 감지 → 인사
    ↓
각 스팟마다 (6개 스팟):
    - 도착 안내
    - 스팟 소개 (TTS)
    - Q&A 세션 (10초 타임아웃)
    - 포토 스팟 확인 (해당되는 경우)
    ↓
투어 완료 메시지
```

## 📁 프로젝트 구조

```
dori-project/
├── app/
│   ├── dori_main.py              # 진입점: 웨이크워드 감지 → 투어 시작
│   ├── main_tour_loop.py         # 메인 투어 오케스트레이션 로직
│   ├── tour_route.py             # 투어 경로 정의 (6개 스팟)
│   ├── stt_service.py            # Whisper (오프라인 STT)
│   ├── tts_service.py            # Google Cloud Text-to-Speech
│   ├── wakeword_service.py       # 웨이크워드 감지 ("Hey Dori")
│   ├── translation_service.py    # LLM 기반 번역
│   ├── llm_client.py             # 로컬 LLM 인터페이스 (LM Studio/Ollama)
│   ├── rag_pipeline.py           # RAG 컨텍스트 구축
│   ├── faiss_retriever.py       # FAISS 벡터 검색
│   ├── embedding_client.py      # 듀얼 임베딩 모델
│   ├── db_utils.py              # PostgreSQL CRUD 작업
│   ├── config.py                # 설정 (RAG 토글, DB 설정)
│   ├── 00_init_db.py            # 데이터베이스 초기화
│   ├── 01_seed_spots.py         # 스팟 데이터 시드
│   ├── 02_seed_knowledge_docs.py # 지식 베이스 시드
│   └── 03_build_faiss_index.py   # FAISS 인덱스 구축
├── db/
│   ├── schema.sql               # 데이터베이스 스키마
│   └── sample_data.sql          # 샘플 데이터
├── faiss_index_en.bin           # FAISS 벡터 인덱스
├── faiss_ids_en.npy             # FAISS 문서 ID
├── requirements.txt             # Python 의존성
└── README.md                    # 이 파일
```

## 🚀 설치 방법

### 사전 요구사항
- Python 3.11+
- PostgreSQL 데이터베이스
- TTS용 Google Cloud 자격 증명 (선택사항, TTS에만 필요)
- 로컬 LLM 서버 (LM Studio / Ollama)

### 1. 클론 및 의존성 설치

```bash
# 가상 환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 설정

```bash
# 데이터베이스 생성
psql -U postgres -c "CREATE DATABASE dori;"

# 스키마 초기화
psql -U postgres -d dori -f db/schema.sql
psql -U postgres -d dori -f db/sample_data.sql
```

### 3. 환경 설정

```bash
# Google Cloud 자격 증명 설정 (TTS에만 필요)
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/gcp-service-account.json

# app/config.py에서 데이터베이스 자격 증명 업데이트
# DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
```

**참고**: STT는 Whisper(오프라인)를 사용하므로 음성 인식에는 클라우드 자격 증명이 필요하지 않습니다. Google Cloud 자격 증명은 TTS(음성 합성)에만 필요합니다.

### 4. 데이터 시드 및 인덱스 구축

```bash
# 스팟 시드
python app/01_seed_spots.py

# 지식 문서 시드
python app/02_seed_knowledge_docs.py

# FAISS 인덱스 구축
python app/03_build_faiss_index.py
```

### 5. 로컬 LLM 서버 시작

**옵션 A: LM Studio**
- LM Studio 다운로드 및 설치
- 모델 로드: `Llama-3.1-8B-Instruct-GGUF`
- `http://127.0.0.1:1234`에서 로컬 서버 시작

**옵션 B: Ollama**
```bash
ollama pull llama3.1:8b
ollama serve
```

### 6. 애플리케이션 실행

```bash
python app/dori_main.py
```

## 🎯 사용 방법

### 투어 시작하기

1. **웨이크워드 활성화**: "Hey Dori" (영어) 또는 "도리야" (한국어)라고 말하기
2. **언어 감지**: 시스템이 자동으로 언어를 감지합니다
3. **투어 시작**: 로봇이 인사하고 투어를 시작합니다

### 투어 중

- **스팟 소개**: 로봇이 각 위치에 대한 정보를 내레이션합니다
- **Q&A 세션**: 각 스팟 소개 후 질문하기
  - "질문이 있으신가요?" 프롬프트 대기
  - 질문하기 (10초 타임아웃)
  - 로봇이 RAG + LLM을 사용하여 답변
  - "패스"라고 말하여 질문 건너뛰기
- **포토 스팟**: 지정된 위치에서 로봇이 사진 촬영을 안내합니다

### 투어 경로

투어는 다음 6개 스팟을 순서대로 방문합니다:
1. **광화문** (Gwanghwamun) - 정문
2. **흥례문** (Heungnyemun) - 두 번째 문
3. **근정문** (Geunjeongmun) - 세 번째 문
4. **근정전** (Geunjeongjeon) - 정전
5. **수정전** (Sujeongjeon) - 토론 전각
6. **경회루** (Gyeonghoeru) - 포토 스팟 누각

## ⚙️ 설정

### RAG 토글

`app/config.py`를 편집하여 RAG를 활성화/비활성화합니다:

```python
ENABLE_RAG = True   # 맥락 인식 답변을 위해 지식 베이스 사용
ENABLE_RAG = False  # LLM 일반 지식만 사용
```

**RAG가 활성화된 경우:**
- 답변이 knowledge_docs의 컨텍스트를 사용합니다
- 더 정확하고 사이트별 정보를 제공합니다
- 역사/문화 질문을 더 잘 처리합니다

**RAG가 비활성화된 경우:**
- LLM이 일반 지식만 사용합니다
- 더 빠른 응답 (검색 단계 없음)
- 답변 품질 비교에 유용합니다

### 데이터베이스 설정

`app/config.py`에서 데이터베이스 자격 증명을 업데이트합니다:

```python
DB_HOST = "localhost"
DB_NAME = "dori"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
```

## 📊 현재 상태

### 완료: ~85%
- ✅ 핵심 인프라 및 데이터베이스
- ✅ 다국어 지원 시스템 (8개 언어)
- ✅ 음성 서비스 (STT/TTS)
- ✅ 웨이크워드 감지
- ✅ 투어 루프 및 내비게이션
- ✅ RAG를 사용한 Q&A
- ✅ 지식 베이스 (30개 이상의 문서)
- ✅ 포토 스팟 프레임워크

### 진행 중: ~15%
- ⏳ 하드웨어 통합 (내비게이션, 카메라)
- ⏳ 향상된 웨이크워드 (Porcupine/Whisper)
- ⏳ Unitree Go2 프로덕션 배포
- ⏳ GPS 기반 내비게이션을 위한 센서 융합

## 🔮 향후 작업

### 우선순위 1: 하드웨어 통합
- GPS 기반 자율주행 내비게이션
- 사진 촬영을 위한 카메라 통합
- Unitree Go2 제어 시스템 통합

### 우선순위 2: 프로덕션 준비
- Unitree Go2 + NVIDIA Orin에 배포
- 성능 최적화
- 향상된 오류 처리

### 우선순위 3: 기능 향상
- Porcupine 웨이크워드 통합
- 향상된 RAG 컨텍스트 필터링
- 사용자 피드백 분석 시스템
- 추가 언어 지원

## 🧪 RAG 유틸리티 테스트

RAG 활성화 vs 비활성화 응답을 비교하려면:

1. **RAG 활성화**: `config.py`에서 `ENABLE_RAG = True` 설정
2. **테스트 질문**: 사이트별 질문하기 (예: "근정전은 언제 지어졌나요?")
3. **RAG 비활성화**: `ENABLE_RAG = False` 설정
4. **동일한 질문 테스트**: 답변 품질과 정확도 비교

## 📝 주요 설계 결정 사항

1. **영어를 소스 언어로**: 모든 콘텐츠를 영어로 저장하고 런타임에 번역
2. **Q&A용 RAG**: 지식 베이스에서 정확하고 맥락 인식 답변 보장
3. **로컬 LLM**: 프라이버시 및 오프라인 기능
4. **오프라인 STT**: Whisper가 클라우드 의존성 없이 오프라인 음성 인식 제공
5. **모듈식 아키텍처**: 새로운 스팟, 언어 또는 기능을 쉽게 확장 가능
6. **고유명사 정규화**: 궁궐 이름의 잘못된 발음 처리

## 🤝 기여하기

이것은 졸업 프로젝트입니다. 질문이나 기여가 있으시면 프로젝트 팀에 문의해 주세요.

## 📄 라이선스

[라이선스를 여기에 명시하세요]

## 🙏 감사의 말

- **Q&A & 다국어 시스템**: [팀원]
- **사진 촬영 모듈**: Minseo
- **자율주행 내비게이션**: [팀원]

---

**기관**: [귀하의 대학/기관]  
**날짜**: 2024
