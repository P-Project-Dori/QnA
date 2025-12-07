# 02_seed_scripts.py

from db_utils import insert_script_for_spot_code

# TODO: 아래 텍스트들을 네가 실제로 작성한 영어 멘트로 교체하면 됨.
SPOT_SCRIPTS = {
    "gwanghwamun": [
        "This is Gwanghwamun Gate, the main southern gate of Gyeongbokgung Palace.",
        "You are now standing where major state ceremonies and royal processions once took place.",
    ],
    "heungnyemun": [
        "This is Heungnyemun Gate, the second inner gate that leads you deeper into the palace grounds.",
    ],
    "geunjeongmun": [
        "Geunjeongmun Gate leads directly to Geunjeongjeon, the main throne hall of the palace.",
    ],
    "geunjeongjeon": [
        "Geunjeongjeon Hall is where the king held formal audiences and important state ceremonies.",
    ],
    "sujeongjeon": [
        "Sujeongjeon Hall served as an important working space for high-ranking officials and royal secretaries.",
    ],
    "gyeonghoeru": [
        "Gyeonghoeru Pavilion was used for royal banquets and diplomatic receptions, surrounded by a scenic pond.",
    ],
}


def main():
    for spot_code, paragraphs in SPOT_SCRIPTS.items():
        for idx, text_en in enumerate(paragraphs, start=1):
            insert_script_for_spot_code(spot_code, idx, text_en)
    print("✅ SPOT_SCRIPTS 기준 scripts 데이터 입력 완료!")


if __name__ == "__main__":
    main()
