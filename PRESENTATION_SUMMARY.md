# DORI Project - Presentation Summary

## 📋 Project Overview

**DORI (다국어 관광 안내 로봇)** - Multilingual Autonomous Tour Guide Robot
- **Goal**: Autonomous robot that guides tourists through Gyeongbokgung Palace
- **Target**: Complete demo with spot narration, Q&A, photo spots, and wakeword activation
- **Hardware**: Unitree Go2 + NVIDIA Orin (planned deployment)

---

## ✅ Completed Features

### 1. **Core Architecture & Database**
- ✅ PostgreSQL database schema fully designed and implemented
  - Hierarchical structure: Places → Spots → Scripts
  - Knowledge base for RAG (knowledge_docs)
  - Q&A logging system (qa_logs)
  - Multilingual support infrastructure (8 languages)
- ✅ Database initialization scripts (`00_init_db.py`)
- ✅ Data seeding pipeline (spots, scripts, knowledge_docs)

### 2. **Multilingual Support System**
- ✅ **8 Languages Supported**: English, Korean, Japanese, Chinese, French, Spanish, Vietnamese, Thai
- ✅ Translation service using LLM (runtime translation)
- ✅ Translation caching system (script_translations table)
- ✅ Language auto-detection from wakeword

### 3. **Speech Services**
- ✅ **STT (Speech-to-Text)**: Google Cloud Speech-to-Text integration
  - Multi-language recognition
  - Real-time audio processing
- ✅ **TTS (Text-to-Speech)**: Google Cloud Text-to-Speech integration
  - Natural voice synthesis
  - Language-specific voice models

### 4. **Wakeword Detection**
- ✅ Voice-based wakeword detection ("Hey Dori" / "도리야")
- ✅ Fuzzy matching for pronunciation variations
- ✅ Language auto-detection from wakeword
- ✅ Cooldown mechanism to prevent duplicate triggers
- ✅ Fallback console mode for testing

### 5. **Tour Loop System**
- ✅ Complete tour orchestration (`main_tour_loop.py`)
- ✅ Sequential spot navigation (6 spots: Gwanghwamun → Heungnyemun → Geunjeongmun → Geunjeongjeon → Sujeongjeon → Gyeonghoeru)
- ✅ Spot introduction with TTS narration
- ✅ Automatic progression (10-second timeout)
- ✅ Inline wakeword interrupt handling

### 6. **Q&A System**
- ✅ **RAG Pipeline**: 
  - FAISS vector search index
  - Dual embedding models (e5-small-v2 + gte-small)
  - Context retrieval from knowledge_docs
- ✅ **LLM Integration**: Local LLM via LM Studio (Llama-3.1-8B-Instruct)
- ✅ Question normalization (proper noun handling)
- ✅ Multi-turn Q&A support
- ✅ "Pass" command to skip questions

### 7. **Knowledge Base**
- ✅ Comprehensive knowledge_docs for all 6 spots
- ✅ Historical facts, architecture details, cultural context
- ✅ FAISS index built and operational
- ✅ Embedding-based semantic search

### 8. **Photo Spot Feature**
- ✅ Photo spot detection and announcement
- ✅ Positioning instructions
- ✅ Countdown system
- ⚠️ Camera integration pending (TODO in code)

### 9. **Development Infrastructure**
- ✅ Docker containerization setup
- ✅ Database utilities and CRUD operations
- ✅ Proper noun normalization (fuzzy matching for palace names)
- ✅ Error handling and graceful degradation

---

## 🚧 In Progress / Planned Features

### 1. **Hardware Integration**
- ⏳ **Autonomous Navigation**: GPS-based movement between spots
- ⏳ **Camera Integration**: Actual photo capture (currently placeholder)
- ⏳ **Unitree Go2 Integration**: Robot control and movement commands

### 2. **Enhanced Wakeword**
- ⏳ **Porcupine Integration**: More robust wakeword detection
- ⏳ **Whisper Integration**: Improved language detection

### 3. **RAG Improvements**
- ⏳ **Context Filtering**: Better spot-specific context retrieval
- ⏳ **Answer Quality**: Fine-tuning RAG prompts for better accuracy

### 4. **Additional Features**
- ⏳ **More Languages**: Expand beyond current 8 languages
- ⏳ **User Feedback System**: Collect and analyze qa_logs for improvements
- ⏳ **Multiple Tour Routes**: Support for other palaces/locations

---

## 🏗️ Technical Architecture

### **Technology Stack**
- **Language**: Python 3.11
- **Database**: PostgreSQL + psycopg2
- **STT/TTS**: Google Cloud Speech-to-Text / Text-to-Speech
- **RAG**: FAISS + e5-small-v2 + gte-small embeddings
- **LLM**: Local LLM (LM Studio / Ollama / llama.cpp)
- **Deployment**: Docker / docker-compose
- **Hardware**: Unitree Go2 + NVIDIA Orin

### **Data Flow**
```
Wakeword Detection → Language Detection → Tour Start
    ↓
Spot Arrival → Script Retrieval (DB) → Translation → TTS
    ↓
Q&A Session → STT → Translation → RAG Search → LLM → Translation → TTS
    ↓
Photo Spot → Camera Capture (TODO)
    ↓
Next Spot → Repeat
```

### **Key Design Decisions**
1. **English as Source Language**: All content stored in English, translated at runtime
2. **RAG for Q&A**: Ensures accurate, context-aware answers
3. **Local LLM**: Privacy and offline capability
4. **Modular Architecture**: Easy to extend and maintain

---

## 📊 Current Status Summary

### **Completed**: ~85%
- ✅ Core infrastructure and database
- ✅ Multilingual support system
- ✅ Speech services (STT/TTS)
- ✅ Wakeword detection
- ✅ Tour loop and navigation
- ✅ Q&A with RAG
- ✅ Knowledge base
- ✅ Photo spot framework

### **Remaining**: ~15%
- ⏳ Hardware integration (navigation, camera)
- ⏳ Enhanced wakeword (Porcupine/Whisper)
- ⏳ Production deployment on Unitree Go2

---

## 🎯 Next Steps

1. **Hardware Integration** (Priority 1)
   - Implement GPS-based navigation
   - Connect camera for photo capture
   - Integrate with Unitree Go2 control system

2. **Production Readiness** (Priority 2)
   - Deploy on Unitree Go2 + NVIDIA Orin
   - Performance optimization
   - Error handling improvements

3. **Feature Enhancement** (Priority 3)
   - Porcupine wakeword integration
   - Enhanced RAG context filtering
   - User feedback analysis system

---

## 💡 Key Achievements

1. **Complete End-to-End Pipeline**: From wakeword to tour completion
2. **Multilingual Support**: 8 languages with runtime translation
3. **RAG-Based Q&A**: Accurate, context-aware answers
4. **Scalable Architecture**: Easy to add new spots, languages, or features
5. **Production-Ready Codebase**: Well-structured, documented, containerized

---

## 📈 Demo Capabilities

The current system can demonstrate:
- ✅ Wakeword activation ("Hey Dori" / "도리야")
- ✅ Language auto-detection
- ✅ Tour narration in multiple languages
- ✅ Interactive Q&A with RAG
- ✅ Photo spot announcements
- ✅ Multi-turn conversations
- ✅ Proper noun recognition (palace names)

---

## 🔮 Future Vision

- Expand to multiple palaces and tourist sites
- Support for more languages (10+)
- Advanced navigation with obstacle avoidance
- Real-time photo sharing with tourists
- Analytics dashboard for tour insights
- Mobile app integration for user experience









