# 🐧 DORI — Multilingual Autonomous Tour Guide Robot

**DORI (다국어 관광 안내 로봇)** is an autonomous tour guide robot system designed to provide multilingual guidance to tourists visiting cultural heritage sites, specifically Gyeongbokgung Palace in Seoul, South Korea.

## 📋 Project Overview

DORI integrates three core modules:
1. **Multilingual Q&A System** with RAG-based LLM for intelligent question answering
2. **Photographer Dori** for automated tourist photography (framework implemented)
3. **Autonomous Navigation** using sensor fusion (planned)

The system supports **8 languages** (English, Korean, Japanese, Chinese, French, Spanish, Vietnamese, Thai) and provides real-time speech-to-speech interaction with context-aware answers using Retrieval-Augmented Generation (RAG).

## ✅ Completed Features

### Core Infrastructure
- ✅ **PostgreSQL Database**: Hierarchical structure (Places → Spots → Scripts)
- ✅ **Knowledge Base**: 30+ knowledge documents for RAG
- ✅ **FAISS Vector Index**: Fast semantic search for context retrieval
- ✅ **Dual Embedding Models**: e5-small-v2 + gte-small for enhanced retrieval

### Multilingual Support
- ✅ **8 Languages**: English, Korean, Japanese, Chinese, French, Spanish, Vietnamese, Thai
- ✅ **Runtime Translation**: LLM-based translation pipeline
- ✅ **Translation Caching**: Optimized performance with cached translations
- ✅ **Language Auto-Detection**: Automatic detection from wakeword

### Speech Services
- ✅ **STT (Speech-to-Text)**: Google Cloud Speech-to-Text integration
- ✅ **TTS (Text-to-Speech)**: Google Cloud Text-to-Speech with natural voice synthesis
- ✅ **Multi-language Recognition**: Supports all 8 languages

### Wakeword Detection
- ✅ **Voice-based Detection**: "Hey Dori" (English) / "도리야" (Korean)
- ✅ **Fuzzy Matching**: Handles pronunciation variations using Levenshtein distance
- ✅ **Language Auto-Detection**: Determines user language from wakeword
- ✅ **Cooldown Mechanism**: Prevents duplicate triggers

### Tour Loop System
- ✅ **Complete Tour Orchestration**: Sequential navigation through 6 spots
- ✅ **Spot Introduction**: TTS narration for each location
- ✅ **Q&A Sessions**: Interactive question-answering with 10-second timeout
- ✅ **Inline Wakeword Interrupt**: Users can interrupt during narration
- ✅ **Automatic Progression**: Moves to next spot if no questions

### Q&A System with RAG
- ✅ **RAG Pipeline**: FAISS-based semantic search from knowledge base
- ✅ **LLM Integration**: Local LLM via LM Studio (Llama-3.1-8B-Instruct)
- ✅ **Proper Noun Normalization**: Handles mispronunciations of palace names
- ✅ **Multi-turn Q&A**: Supports follow-up questions
- ✅ **"Pass" Command**: Users can skip questions
- ✅ **RAG Toggle**: Can enable/disable RAG via config flag

### Photo Spot Feature
- ✅ **Photo Spot Detection**: Identifies designated photo locations
- ✅ **Positioning Instructions**: Guides users to optimal positions
- ✅ **Countdown System**: 5-second countdown before capture
- ⚠️ **Camera Integration**: Framework ready, hardware integration pending

## 🏗️ System Architecture

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Programming Language** | Python 3.11 |
| **Database** | PostgreSQL + psycopg2 |
| **Speech Recognition** | Google Cloud Speech-to-Text |
| **Speech Synthesis** | Google Cloud Text-to-Speech |
| **LLM** | Local LLM (LM Studio / Ollama / llama.cpp) |
| **RAG** | FAISS + e5-small-v2 + gte-small embeddings |
| **Deployment** | Docker / docker-compose |
| **Hardware** | Unitree Go2 Quadruped Robot + NVIDIA Orin |

### Data Flow

**Q&A Pipeline:**
```
User Speech → STT (Google) → Language Detection
    ↓
Translation (User Lang → English) → RAG Context Retrieval
    ↓
LLM Answer Generation → Translation (English → User Lang)
    ↓
TTS (Google Cloud) → Audio Output
```

**Tour Flow:**
```
Wakeword Detection → Language Auto-Detection → Greeting
    ↓
For each spot (6 spots):
    - Arrival Announcement
    - Spot Introduction (TTS)
    - Q&A Session (10s timeout)
    - Photo Spot Check (if applicable)
    ↓
Tour Completion Message
```

## 📁 Project Structure

```
dori-project/
├── app/
│   ├── dori_main.py              # Entry point: wakeword detection → tour start
│   ├── main_tour_loop.py         # Main tour orchestration logic
│   ├── tour_route.py             # Tour route definition (6 spots)
│   ├── stt_service.py            # Google Cloud Speech-to-Text
│   ├── tts_service.py            # Google Cloud Text-to-Speech
│   ├── wakeword_service.py       # Wakeword detection ("Hey Dori")
│   ├── translation_service.py    # LLM-based translation
│   ├── llm_client.py             # Local LLM interface (LM Studio/Ollama)
│   ├── rag_pipeline.py           # RAG context building
│   ├── faiss_retriever.py       # FAISS vector search
│   ├── embedding_client.py      # Dual embedding models
│   ├── db_utils.py              # PostgreSQL CRUD operations
│   ├── config.py                # Configuration (RAG toggle, DB settings)
│   ├── 00_init_db.py            # Database initialization
│   ├── 01_seed_spots.py         # Seed spot data
│   ├── 02_seed_knowledge_docs.py # Seed knowledge base
│   └── 03_build_faiss_index.py   # Build FAISS index
├── db/
│   ├── schema.sql               # Database schema
│   └── sample_data.sql          # Sample data
├── faiss_index_en.bin           # FAISS vector index
├── faiss_ids_en.npy             # FAISS document IDs
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Google Cloud credentials for STT/TTS
- Local LLM server (LM Studio / Ollama)

### 1. Clone and Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create database
psql -U postgres -c "CREATE DATABASE dori;"

# Initialize schema
psql -U postgres -d dori -f db/schema.sql
psql -U postgres -d dori -f db/sample_data.sql
```

### 3. Configure Environment

```bash
# Set Google Cloud credentials
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/gcp-service-account.json

# Update database credentials in app/config.py
# DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
```

### 4. Seed Data and Build Index

```bash
# Seed spots
python app/01_seed_spots.py

# Seed knowledge documents
python app/02_seed_knowledge_docs.py

# Build FAISS index
python app/03_build_faiss_index.py
```

### 5. Start Local LLM Server

**Option A: LM Studio**
- Download and install LM Studio
- Load model: `Llama-3.1-8B-Instruct-GGUF`
- Start local server on `http://127.0.0.1:1234`

**Option B: Ollama**
```bash
ollama pull llama3.1:8b
ollama serve
```

### 6. Run the Application

```bash
python app/dori_main.py
```

## 🎯 Usage

### Starting a Tour

1. **Wakeword Activation**: Say "Hey Dori" (English) or "도리야" (Korean)
2. **Language Detection**: System automatically detects your language
3. **Tour Begins**: Robot greets you and starts the tour

### During the Tour

- **Spot Introductions**: Robot narrates information about each location
- **Q&A Sessions**: Ask questions after each spot introduction
  - Wait for "Do you have any questions?" prompt
  - Ask your question (10-second timeout)
  - Robot answers using RAG + LLM
  - Say "pass" to skip questions
- **Photo Spots**: At designated locations, robot will guide you for photos

### Tour Route

The tour visits 6 spots in order:
1. **Gwanghwamun** (광화문) - Main gate
2. **Heungnyemun** (흥례문) - Second gate
3. **Geunjeongmun** (근정문) - Third gate
4. **Geunjeongjeon** (근정전) - Main throne hall
5. **Sujeongjeon** (수정전) - Discussion hall
6. **Gyeonghoeru** (경회루) - Photo spot pavilion

## ⚙️ Configuration

### RAG Toggle

Edit `app/config.py` to enable/disable RAG:

```python
ENABLE_RAG = True   # Use knowledge base for context-aware answers
ENABLE_RAG = False  # Use LLM general knowledge only
```

**When RAG is enabled:**
- Answers use context from knowledge_docs
- More accurate, site-specific information
- Better handling of historical/cultural questions

**When RAG is disabled:**
- LLM uses general knowledge only
- Faster response (no retrieval step)
- Useful for comparing answer quality

### Database Configuration

Update `app/config.py` with your database credentials:

```python
DB_HOST = "localhost"
DB_NAME = "dori"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
```

## 📊 Current Status

### Completed: ~85%
- ✅ Core infrastructure and database
- ✅ Multilingual support system (8 languages)
- ✅ Speech services (STT/TTS)
- ✅ Wakeword detection
- ✅ Tour loop and navigation
- ✅ Q&A with RAG
- ✅ Knowledge base (30+ documents)
- ✅ Photo spot framework

### In Progress: ~15%
- ⏳ Hardware integration (navigation, camera)
- ⏳ Enhanced wakeword (Porcupine/Whisper)
- ⏳ Production deployment on Unitree Go2
- ⏳ Sensor fusion for GPS-based navigation

## 🔮 Future Work

### Priority 1: Hardware Integration
- GPS-based autonomous navigation
- Camera integration for photo capture
- Unitree Go2 control system integration

### Priority 2: Production Readiness
- Deploy on Unitree Go2 + NVIDIA Orin
- Performance optimization
- Enhanced error handling

### Priority 3: Feature Enhancement
- Porcupine wakeword integration
- Enhanced RAG context filtering
- User feedback analysis system
- Support for additional languages

## 🧪 Testing RAG Utility

To compare RAG-enabled vs RAG-disabled responses:

1. **Enable RAG**: Set `ENABLE_RAG = True` in `config.py`
2. **Test Questions**: Ask site-specific questions (e.g., "When was Geunjeongjeon built?")
3. **Disable RAG**: Set `ENABLE_RAG = False`
4. **Test Same Questions**: Compare answer quality and accuracy

## 📝 Key Design Decisions

1. **English as Source Language**: All content stored in English, translated at runtime
2. **RAG for Q&A**: Ensures accurate, context-aware answers from knowledge base
3. **Local LLM**: Privacy and offline capability
4. **Modular Architecture**: Easy to extend with new spots, languages, or features
5. **Proper Noun Normalization**: Handles mispronunciations of palace names

## 🤝 Contributing

This is a graduation project. For questions or contributions, please contact the project team.

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- **Q&A & Multilingual System**: [Team Member]
- **Photography Module**: Minseo
- **Autonomous Navigation**: [Team Member]

---

**Institution**: [Your University/Institution]  
**Date**: 2024
