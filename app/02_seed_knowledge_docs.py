# 02_seed_knowledge_docs.py

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
                "Heungnyemun is the central gate of Gyeongbokgung Palace. "
                "'Heungnye' means 'to raise up rites.' Originally called 'Hongnyemun,' "
                "it was renamed to its current name in 1867 (the 4th year of King Gojong's reign) "
                "during the reconstruction of Gyeongbokgung Palace."
            ),
            "source_type": "extra",
            "source_ref": "wiki:heungnyemun:overview",
            "tags": ["gate", "history", "naming"],
        },
        {
            "text": (
                "Heungnyemun was demolished during the Japanese colonial period to make way for "
                "the construction of the Government-General of Korea building. "
                "Following the demolition of the building in 1996, it was restored in 2001."
            ),
            "source_type": "extra",
            "source_ref": "wiki:heungnyemun:restoration",
            "tags": ["restoration", "history", "colonial period"],
        },
        {
            "text": (
                "In the center of the Heungnyemun area, the Geumcheon Stream, a stream flowing from Baekaksan Mountain, flows, "
                "and over it flows the Yeongjegyo Bridge. Yeongjegyo Bridge, named after King Sejong, "
                "survived the Imjin War without significant damage and was restored in 1867 during the reconstruction of Gyeongbokgung Palace."
            ),
            "source_type": "extra",
            "source_ref": "wiki:heungnyemun:yeongjegyo",
            "tags": ["bridge", "stream", "history", "architecture"],
        },
        {
            "text": (
                "Yeongjegyo Bridge was demolished along with Heungnyemun Gate during the Japanese colonial period "
                "and restored in 2001."
            ),
            "source_type": "extra",
            "source_ref": "wiki:heungnyemun:yeongjegyo_restoration",
            "tags": ["bridge", "restoration", "history"],
        },
    ],
    "geunjeongmun": [
        {
            "text": (
                "Geunjeongmun Gate is the main gate of Geunjeongjeon Hall. "
                "It features a hipped roof with three bays at the front and two bays at the side. "
                "It is the only main gate of a palace main hall with a two-story structure."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongmun:architecture",
            "tags": ["gate", "architecture", "structure"],
        },
        {
            "text": (
                "Geunjeongmun was used for royal funerals and coronations, and the successors to the throne were crowned here, "
                "including Danjong, Seongjong, and Myeongjong. Geunjeongmun, including its corridors, was designated a Treasure in 1985."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongmun:history",
            "tags": ["ceremony", "coronation", "history", "treasure"],
        },
    ],
    "geunjeongjeon": [
        {
            "text": (
                "Geunjeongjeon Hall is the main hall of Gyeongbokgung Palace. "
                "It was used for important state events, such as the king's coronation, ceremonies for court officials, "
                "receptions of foreign envoys, and royal banquets. The name 'Geunjeong' in Geunjeongjeon means 'to diligently govern the world.' "
                "It is the largest and most formal building in the palace, occupying the largest area."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:overview",
            "tags": ["throne hall", "ceremony", "national events", "meaning"],
        },
        {
            "text": (
                "Geunjeongjeon is constructed on a two-tiered stone platform, with a lower pedestal atop it, creating a two-story structure. "
                "From the inside, it appears as a single, uninterrupted structure."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:architecture",
            "tags": ["architecture", "structure", "platform"],
        },
        {
            "text": (
                "The front yard of Geunjeongjeon, or the court, is paved with slabs of stone, much like those of other palaces. "
                "Its central corridor, three paths, embody the formality of a palace. Within the court, the rank stones for ranks 1st through 9th are placed."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:courtyard",
            "tags": ["courtyard", "architecture", "formality", "rank stones"],
        },
        {
            "text": (
                "The corners of the Woldae Pavilion and the balustrades surrounding the stairs are adorned with simple yet ingenious carvings "
                "of the Four Guardian Gods, the Twelve Zodiac Signs, and the 28 constellations."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:decorations",
            "tags": ["decorations", "carvings", "symbolism", "guardian gods"],
        },
        {
            "text": (
                "The interior floor is paved with brick, and the royal throne is located in the center of the north. "
                "Behind the throne is the 'Ilwol Obongdo,' a painting depicting the sun, moon, and five peaks, symbolizing royal authority. "
                "The ceiling is adorned with carvings of seven dragons."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:interior",
            "tags": ["interior", "throne", "painting", "symbolism", "dragons"],
        },
        {
            "text": (
                "King Jeongjong, Sejong, Sejo, Jungjong, and Seonjo ascended the throne at Geunjeongjeon Hall, "
                "and it was designated a National Treasure in 1985."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:history",
            "tags": ["history", "kings", "national treasure"],
        },
        {
            "text": (
                "The column-linked pilasters of Geunjeongjeon Hall contain inscriptions emphasizing values such as: "
                "establishing love and fostering close ties between relatives, loving learning and enjoying good deeds, "
                "maintaining clear order of the six relatives, extending virtue to the nine clans, and being cautious about leisure and pleasure."
            ),
            "source_type": "extra",
            "source_ref": "wiki:geunjeongjeon:inscriptions",
            "tags": ["inscriptions", "philosophy", "values", "confucianism"],
        },
    ],
    "sujeongjeon": [
        {
            "text": (
                "The 'Sujeong' in Sujeongjeon Hall means 'to conduct politics well.' "
                "This building served as a side hall during the reign of King Gojong. "
                "It wasn't present when Gyeongbokgung Palace was first built, but was added during the reconstruction of the palace."
            ),
            "source_type": "extra",
            "source_ref": "wiki:sujeongjeon:overview",
            "tags": ["meaning", "history", "construction", "king gojong"],
        },
        {
            "text": (
                "In 1894 (the 31st year of King Gojong's reign), during the Gabo Reforms, the Office of Military Affairs was established here. "
                "Later, when the Uijeongbu was transformed into the Naegak, it served as the cabinet's headquarters."
            ),
            "source_type": "extra",
            "source_ref": "wiki:sujeongjeon:gabo_reforms",
            "tags": ["gabo reforms", "military affairs", "cabinet", "politics"],
        },
        {
            "text": (
                "Notably, during the early Joseon Dynasty, the area around Sujeongjeon Hall was home to the Jiphyeonjeon Hall, "
                "the birthplace of the Hunminjeongeum (Korean alphabet) during the reign of King Sejong."
            ),
            "source_type": "extra",
            "source_ref": "wiki:sujeongjeon:jiphyeonjeon",
            "tags": ["jiphyeonjeon", "hunminjeongeum", "king sejong", "korean alphabet"],
        },
        {
            "text": (
                "Sujeongjeon Hall was designated a Treasure in 2012."
            ),
            "source_type": "extra",
            "source_ref": "wiki:sujeongjeon:designation",
            "tags": ["treasure", "designation"],
        },
    ],
    "gyeonghoeru": [
        {
            "text": (
                "The 'Gyeonghoe' in Gyeonghoeru Pavilion means 'celebrated banquet.' "
                "This pavilion is located within a pond to the west of the main living quarters of Gyeongbokgung Palace. "
                "Gyeonghoeru Pavilion was where the king held grand banquets with his subjects and entertained foreign envoys."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:overview",
            "tags": ["meaning", "banquet", "location", "diplomacy"],
        },
        {
            "text": (
                "Gyeonghoeru was designed as a royal garden where visitors could enjoy boating on the pond, "
                "climb up to the pavilion, and admire the majestic views of Inwangsan Mountain and the palace."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:garden",
            "tags": ["garden", "scenery", "inwangsan", "recreation"],
        },
        {
            "text": (
                "Initially a small pavilion, it was rebuilt in 1412 (the 12th year of King Taejong's reign) "
                "by digging a large pond and expanding it to its current scale. "
                "It was repaired during the reigns of King Seongjong and King Yeonsangun, "
                "but was destroyed during the Japanese invasions of Korea."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:construction",
            "tags": ["construction", "history", "king taejong", "imjin war"],
        },
        {
            "text": (
                "Gyeonghoeru was rebuilt in 1867 (the 4th year of King Gojong's reign) "
                "during the reconstruction of Gyeongbokgung Palace."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:restoration",
            "tags": ["restoration", "king gojong", "reconstruction"],
        },
        {
            "text": (
                "The first floor of Gyeonghoeru consists of 48 tall stone pillars (24 round and 24 square). "
                "A wooden floor was laid on the second floor, serving as a banquet hall."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:architecture",
            "tags": ["architecture", "pillars", "structure", "banquet hall"],
        },
        {
            "text": (
                "The eaves of the pavilion boast 11 japsang (decorative roof tiles depicting various deities)—"
                "the most of any building in Korea."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:japsang",
            "tags": ["decorations", "japsang", "roof tiles", "deities"],
        },
        {
            "text": (
                "Gyeonghoeru was designated a National Treasure in 1985."
            ),
            "source_type": "extra",
            "source_ref": "wiki:gyeonghoeru:designation",
            "tags": ["national treasure", "designation"],
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

