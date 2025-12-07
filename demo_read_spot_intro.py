# demo_read_spot_intro.py

from tts_utils import tts_play, UserLang
from db_utils import get_scripts_for_spot_code


def build_spot_intro_text_en(spot_code: str) -> str:
    """
    주어진 스팟 코드에 해당하는 영어 스크립트를 DB에서 읽어서
    하나의 긴 영어 텍스트로 합쳐 반환한다.

    get_scripts_for_spot_code 예시:
      get_scripts_for_spot_code("GWANGHWAMUN")
      -> [(1, "Gwanghwamun is ..."), (2, "It was built in ..."), ...]
    """
    scripts = get_scripts_for_spot_code(spot_code)
    paragraphs = [text_en for _, text_en in scripts]
    return "\n\n".join(paragraphs)


def run_demo_for_spot(spot_code: str, user_lang: UserLang = "en") -> None:
    """
    1) 해당 스팟의 영어 스크립트를 DB에서 읽어오고
    2) 현재 단계에서는 영어 그대로 TTS로 읽어준다.

    나중에 다국어를 붙이고 싶으면:
    - intro_text_en을 translate(intro_text_en, "en", user_lang)으로 변환해서
      user_lang에 맞는 텍스트를 만든 후 tts_play에 넘기면 된다.
    """
    intro_text_en = build_spot_intro_text_en(spot_code)

    if not intro_text_en.strip():
        print(f"[경고] spot_code={spot_code} 에 대한 영어 스크립트가 없습니다.")
        return

    print(f"[INFO] 스팟 {spot_code} 영어 스크립트:")
    print(intro_text_en)
    print()

    # 현재는 영어 스크립트를 영어로 읽어줌
    tts_play(intro_text_en, user_lang="en")


if __name__ == "__main__":
    # 여기에서 테스트할 스팟 코드 지정
    # 예: "GWANGHWAMUN", "HEUNGNYEMUN" 등
    run_demo_for_spot(spot_code="gwanghwamun", user_lang="en")
