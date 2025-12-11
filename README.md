* 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞 𝐒𝐞𝐭𝐮𝐩 & 𝐒𝐞𝐞𝐝𝐢𝐧𝐠 𝐒𝐜𝐫𝐢𝐩𝐭𝐬

01_seed_spots.py : Seeds the spots table from TOUR_ROUTE (spot codes, names, order, photo flags). Inserts Gyeongbokgung Palace tour locations into PostgreSQL.

02_seed_scripts.py : Seeds English tour scripts per spot. Stores paragraph-by-paragraph explanations for each location in the database.

03_seed_knowledge_docs.py : Seeds knowledge documents for RAG. Inserts detailed historical/cultural info per spot with metadata (source, tags) for Q&A retrieval.

04_build_faiss_index.py : Builds the FAISS vector index from knowledge documents. Computes embeddings using e5-small-v2 and gte-small, creates a FAISS index for semantic search, and saves index and document IDs to disk.


* 𝐂𝐨𝐫𝐞 𝐀𝐩𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧 𝐅𝐢𝐥𝐞𝐬
  
dori_main.py : Main entry point. Starts the wakeword listener, detects "Hey Dori" via Whisper STT, sets user language, and triggers the tour loop.

main_tour_loop.py : Orchestrates the tour flow. Manages spot navigation, script reading, Q&A sessions, and photo spots using predefined phrases and database scripts.

tour_route.py : Defines the tour route. Lists all spots in order with multilingual names (Korean, English, Japanese, Chinese, etc.) and marks photo spots.


* 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞 & 𝐂𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧
  
config.py : Database connection settings. Stores PostgreSQL credentials (host, database name, user, password) for the application.

db_utils.py : Database utility functions. Provides context managers for connections and CRUD for spots, scripts, and knowledge documents.


* 𝐒𝐩𝐞𝐞𝐜𝐡 𝐒𝐞𝐫𝐯𝐢𝐜𝐞𝐬

stt_service.py : Speech-to-text using Whisper tiny. Records audio with sounddevice, transcribes with Whisper (offline, CPU), supports language detection, and returns transcript and detected language.

tts_service.py : Text-to-speech using ElevenLabs API. Converts text to speech via ElevenLabs (MP3), plays audio in-memory with pygame.mixer, and supports Korean and English voices.

wakeword_service.py : Wakeword detection service. Continuously listens for "Hey Dori" / "도리야" using fuzzy matching (Levenshtein distance), handles pronunciation variations, and triggers tour start callback.


* 𝐀𝐈 & 𝐑𝐀𝐆 𝐒𝐞𝐫𝐯𝐢𝐜𝐞𝐬
  
llm_client.py : LLM client for LM Studio. Connects to local LM Studio server (port 1234), sends chat completion requests, handles connection errors gracefully, and provides RAG-aware question answering.

translation_service.py : Translation service using LLM. Translates text between supported languages (8 languages), uses LLM for translation, and provides specialized functions for question/answer translation.

embedding_client.py : Embedding generation service. Loads and caches e5-small-v2 model, generates query and passage embeddings for RAG, and formats text with "query:" or "passage:" prefixes.

faiss_retriever.py : FAISS-based document retriever. Loads pre-built FAISS index, performs semantic search on user questions, returns top-k relevant documents, and handles dimension mismatches.

rag_pipeline.py : RAG pipeline orchestrator. Combines FAISS retrieval with spot filtering, builds context from retrieved documents, and prepares context for LLM Q&A.


* 𝐔𝐭𝐢𝐥𝐢𝐭𝐲 & 𝐓𝐞𝐬𝐭 𝐅𝐢𝐥𝐞𝐬

multilingual_orchestrator.py : Multilingual Q&A orchestrator. Handles single Q&A turns: records audio, transcribes, translates question to English, performs RAG+LLM, translates answer back, and plays TTS.
