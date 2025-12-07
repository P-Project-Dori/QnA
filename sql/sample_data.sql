---------------------------------------------
-- sample_data.sql
-- 다국어 관광 안내 로봇(도리) - 초기 데이터 (영어 기준)
---------------------------------------------

-- 1. languages: 지원 언어 (총 8개)
INSERT INTO languages (code, name) VALUES
    ('en', 'English'),
    ('ko', 'Korean'),
    ('zh', 'Chinese'),
    ('ja', 'Japanese'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('vi', 'Vietnamese'),
    ('th', 'Thai')
ON CONFLICT (code) DO NOTHING;

-- 2. places: 관광지(큰 단위) - 다른 궁궐 추가 시 구현(확장성)
INSERT INTO places (id, order_in_tour, title_en, description_en) VALUES
    (
        'gyeongbokgung',
        1,
        'Gyeongbokgung Palace',
        'The main royal palace of the Joseon dynasty and one of the most iconic landmarks in Seoul.'
    )
ON CONFLICT (id) DO NOTHING;