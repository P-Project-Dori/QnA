---------------------------------------------
-- schema.sql (reset & updated)
-- 다국어 관광 안내 로봇(도리) - RDB 스키마
-- ✅ 영어(EN)를 원본 소스로 두고, 다른 언어는 번역+캐시
---------------------------------------------

-- 1. languages: 지원 언어 테이블
CREATE TABLE IF NOT EXISTS languages (
    code        VARCHAR(8) PRIMARY KEY,  -- 'en', 'ko', 'ja', 'zh'
    name        TEXT NOT NULL
);

-- 2. places: 관광지(큰 단위, 예: Gyeongbokgung Palace)
--    👉 영어만 필수. 다른 언어 제목/설명은 런타임 번역 or 별도 캐시.
CREATE TABLE IF NOT EXISTS places (
    id              VARCHAR(64) PRIMARY KEY,   -- 'gyeongbokgung'
    order_in_tour   INTEGER NOT NULL,          -- 투어 순서 (1, 2, 3, ...)
    title_en        TEXT NOT NULL,             -- English title (source)
    description_en  TEXT                       -- English description (source)
);

CREATE INDEX IF NOT EXISTS idx_places_order ON places(order_in_tour);

-- 3. spots: 각 place 안의 스팟
DROP TABLE IF EXISTS spots CASCADE;

CREATE TABLE IF NOT EXISTS spots (
    id          SERIAL PRIMARY KEY,
    place_id    VARCHAR(64) REFERENCES places(id) ON DELETE CASCADE,
    code        VARCHAR(50) NOT NULL,      -- 'gwanghwamun', 'heungnyemun' 등
    name_en     TEXT NOT NULL,
    order_no    INTEGER NOT NULL,
    lat         DOUBLE PRECISION,
    lng         DOUBLE PRECISION,
	is_photo_spot BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_spots_code ON spots(code);

CREATE INDEX IF NOT EXISTS idx_spots_place_order ON spots(place_id, order_no);

-- 4. scripts: TTS로 읽을 문단/문장 (영어 원본)
DROP TABLE IF EXISTS scripts CASCADE;

CREATE TABLE IF NOT EXISTS scripts (
    id              SERIAL PRIMARY KEY,
    spot_id         INTEGER NOT NULL REFERENCES spots(id) ON DELETE CASCADE,
    order_in_spot   INTEGER NOT NULL,
    text_en         TEXT NOT NULL
);

-- 중복 방지를 위해 spot_id + order_in_spot 조합을 유니크하게 강제
CREATE UNIQUE INDEX IF NOT EXISTS uq_scripts_spot_order
    ON scripts(spot_id, order_in_spot);
	
-- 4-1. script_translations: 기본은 영어 → 다른 언어로 번역
DROP TABLE IF EXISTS script_translations CASCADE;

CREATE TABLE IF NOT EXISTS script_translations (
    id              SERIAL PRIMARY KEY,
    script_id       INTEGER NOT NULL REFERENCES scripts(id) ON DELETE CASCADE,
    language        VARCHAR(8) NOT NULL REFERENCES languages(code),
    text_trans      TEXT NOT NULL,
    UNIQUE (script_id, language)
);

CREATE INDEX IF NOT EXISTS idx_script_trans_lang
    ON script_translations(language);
	
-- 5. knowledge_docs: RAG용 문서 (기본 언어 = en)
DROP TABLE IF EXISTS knowledge_docs CASCADE;

CREATE TABLE IF NOT EXISTS knowledge_docs (
    id              SERIAL PRIMARY KEY,
    spot_id         INTEGER REFERENCES spots(id) ON DELETE SET NULL,
    place_id        VARCHAR(64) REFERENCES places(id) ON DELETE SET NULL,
    language        VARCHAR(8) NOT NULL REFERENCES languages(code) DEFAULT 'en',
    source_type     VARCHAR(32) NOT NULL,
    source_ref      TEXT,
    text            TEXT NOT NULL,
    tags            JSONB
);

CREATE INDEX IF NOT EXISTS idx_knowledge_lang
    ON knowledge_docs(language);
	
CREATE INDEX IF NOT EXISTS idx_knowledge_spot_lang
    ON knowledge_docs(spot_id, language);
	
CREATE INDEX IF NOT EXISTS idx_knowledge_place_lang
    ON knowledge_docs(place_id, language);
	
CREATE INDEX IF NOT EXISTS idx_knowledge_source_type
    ON knowledge_docs(source_type);
	
-- 6. qa_logs: Q&A 로그
DROP TABLE IF EXISTS qa_logs CASCADE;

CREATE TABLE IF NOT EXISTS qa_logs (
    id              SERIAL PRIMARY KEY,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_id      TEXT,
    language        VARCHAR(8) REFERENCES languages(code),
    place_id        VARCHAR(64) REFERENCES places(id),
    spot_id         INTEGER REFERENCES spots(id),
    user_question   TEXT NOT NULL,
    llm_answer      TEXT NOT NULL,
    used_doc_ids    INTEGER[],
    user_feedback   SMALLINT
);

CREATE INDEX IF NOT EXISTS idx_qa_logs_created_at
    ON qa_logs(created_at);
	
CREATE INDEX IF NOT EXISTS idx_qa_logs_spot_lang
    ON qa_logs(spot_id, language);
	
---------------------------------------------
-- END OF SCHEMA
---------------------------------------------