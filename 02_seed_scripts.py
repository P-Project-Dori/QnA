# 02_seed_scripts.py

from db_utils import insert_script_for_spot_code

SPOT_SCRIPTS = {
    "gwanghwamun": [
        "Gwanghwamun is the main southern gate of Gyeongbokgung Palace.",
        "This area was once the center of government offices during the Joseon Dynasty.",
        "Although the gate was destroyed several times through wars and colonial rule, it has now been fully restored to its appearance from King Gojong's reconstruction in 1867.",
    ],
    "heungnyemun": [
        "In front of Heungnyemun Gate, royal guards once held ceremonies to change their duties.",
        "During Japanese colonial rule, the gate was demolished and replaced by the Government-General Building.",
        "After its removal in 1995, Heungnyemun was restored, symbolizing the recovery of our national pride.",
    ],
    "geunjeongmun": [
        "Geunjeongmun is the front gate of Geunjeongjeon Hall.",
        "The stone path in front is the king's exclusive passage, called the eodo or 'royal road.'",
        "The phoenix carved into the stone symbolizes peace and the king's authority.",
    ],
    "geunjeongjeon": [
        "Geunjeongjeon is the main hall of Gyeongbokgung Palace, where major state ceremonies were held.",
        "On the front terraces, 36 stone animal figures protect the king from evil spirits, and small guardian figures called japsang watch over the roof.",
        "The iron water vessel placed here, called a deumeu, was used to prevent fires and is tied to legends about chasing away fire spirits.",
    ],
    "sujeongjeon": [
        "Sujeongjeon stands on the site of Jiphyeonjeon, the Hall of Worthies from King Sejong's era.",
        "It was the center of scholarship where brilliant scholars helped refine and promote Hangeul.",
        "Their work led to major advances in science, astronomy, history, music, and literature during Sejong's reign.",
    ],
    "gyeonghoeru": [
        "Gyeonghoeru Pavilion is the largest pavilion of the Joseon Dynasty, built for royal banquets and receptions.",
        "After being rebuilt during King Gojong's reign, bronze dragons were placed in the pond for protection—later rediscovered in 1997.",
        "Bullet marks on the pillars remain from the Korean War.",
        "On clear days, the pavilion's reflection on the water creates a truly breathtaking view.",
    ],
}


def main():
    for spot_code, paragraphs in SPOT_SCRIPTS.items():
        for idx, text_en in enumerate(paragraphs, start=1):
            insert_script_for_spot_code(spot_code, idx, text_en)
    print("✅ SPOT_SCRIPTS 기준 scripts 데이터 입력 완료!")


if __name__ == "__main__":
    main()
