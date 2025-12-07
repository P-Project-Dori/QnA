# 03_seed_knowledge_docs.py

from db_utils import insert_knowledge_doc_for_spot_code

PLACE_ID = "gyeongbokgung"

KNOWLEDGE_DOCS = {
    "gwanghwamun": [
        {
            "text": (
                "Gwanghwamun is the main gate of Gyeongbokgung Palace. "
                "It served as the symbolic entrance to the capital of the Joseon dynasty "
                "and was used for important state ceremonies and the reception of foreign envoys."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gwanghwamun:overview",
            "tags": ["history", "gate", "symbol"],
        },
        {
            "text": (
                "Gwanghwamun has been destroyed and rebuilt multiple times due to wars and occupations. "
                "The current structure was restored in 2010 using traditional wooden construction methods."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gwanghwamun:restoration",
            "tags": ["history", "restoration"],
        },
    ],
    "heungnyemun": [
        {
            "text": (
                "Heungnyemun is the second inner gate of Gyeongbokgung Palace. "
                "It served as the main access point to the administrative courtyard leading to Geunjeongmun and Geunjeongjeon."
            ),
            "source_type": "extra",
            "source_ref": "wiki:heungnyemun:overview",
            "tags": ["gate", "history", "architecture"],
        },
        {
            "text": (
                "Heungnyemun was heavily damaged during the Japanese occupation and later restored as part of "
                "the major reconstruction efforts of Gyeongbokgung in the late 20th century."
            ),
            "source_type": "extra",
            "source_ref": "wiki:heungnyemun:restoration",
            "tags": ["restoration", "history"],
        },
    ],
    "geunjeongmun": [
        {
            "text": (
                "Geunjeongmun is the main gate that leads directly to Geunjeongjeon Hall, "
                "the throne hall of Gyeongbokgung Palace. "
                "It was used by government officials during major state assemblies."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongmun:overview",
            "tags": ["gate", "ceremony", "administration"],
        },
        {
            "text": (
                "The gate reflects the hierarchical structure of Joseon politics, "
                "where officials lined up according to rank during royal ceremonies."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongmun:ceremony",
            "tags": ["tradition", "politics", "culture"],
        },
    ],
    "geunjeongjeon": [
        {
            "text": (
                "Geunjeongjeon is the main throne hall of Gyeongbokgung Palace. "
                "It served as the venue for major national events such as coronations, royal audiences, "
                "and official ceremonies."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:overview",
            "tags": ["throne hall", "ceremony", "national events"],
        },
        {
            "text": (
                "The hall features a double-roof structure and elevated stone terraces symbolizing royal authority "
                "and architectural grandeur during the Joseon dynasty."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:architecture",
            "tags": ["architecture", "symbolism"],
        },
    ],
    "sujeongjeon": [
        {
            "text": (
                "Sujeongjeon Hall was historically used as the royal office where the king conducted daily affairs "
                "of state, including meetings and document reviews."
            ),
            "source_type": "extra",
            "source_ref": "wiki:sujeongjeon:overview",
            "tags": ["office", "politics", "administration"],
        },
        {
            "text": (
                "Sujeongjeon also housed several scholarly activities and served as a place for archiving "
                "important state documents during the Joseon dynasty."
            ),
            "source_type": "extra",
            "source_ref": "wiki:sujeongjeon:history",
            "tags": ["scholarship", "history", "documents"],
        },
    ],
    "gyeonghoeru": [
        {
            "text": (
                "Gyeonghoeru Pavilion is a large banquet hall built on an artificial pond. "
                "It was used for state banquets and receptions of foreign envoys."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:overview",
            "tags": ["banquet", "architecture", "diplomacy"],
        },
        {
            "text": (
                "The structure stands on tall stone pillars and showcases the elegance of Joseon-era architecture, "
                "symbolizing peace, harmony, and national prosperity."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:symbolism",
            "tags": ["symbolism", "architecture"],
        },
    ]
    # 내용 더 추가하기 (출처 확인)
}


def main():
    for spot_code, docs in KNOWLEDGE_DOCS.items():
        for doc in docs:
            insert_knowledge_doc_for_spot_code(
                spot_code=spot_code,
                place_id=PLACE_ID,
                text=doc["text"],
                language="en",
                source_type=doc["source_type"],
                source_ref=doc["source_ref"],
                tags=doc["tags"],
            )
    print("✅ KNOWLEDGE_DOCS 기준 knowledge_docs 데이터 입력 완료!")


if __name__ == "__main__":
    main()
