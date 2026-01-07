# config.py

# Database configuration
DB_HOST = "localhost"
DB_NAME = "dori"   
DB_USER = "postgres"        
DB_PASSWORD = "kk1022"

# ============================================================================
# RAG (Retrieval-Augmented Generation) Configuration
# ============================================================================
# Set to True to enable RAG: LLM answers will use context from knowledge_docs
# Set to False to disable RAG: LLM will answer without context (general knowledge only)
# 
# To compare RAG utility:
#   1. Set ENABLE_RAG = True and test Q&A responses
#   2. Set ENABLE_RAG = False and test the same questions
#   3. Compare answer quality and accuracy
#
# Note: When RAG is disabled, the system will still work but won't use
#       the knowledge base for context-aware answers.
# ============================================================================
ENABLE_RAG = True  # Change to False to disable RAG
