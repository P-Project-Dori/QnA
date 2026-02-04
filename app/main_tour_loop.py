# main_tour_loop.py

import time
import re
from tour_route import TOUR_ROUTE
from stt_service import listen_for_seconds
from tts_service import speak
from llm_client import call_llm
from wakeword_service import is_wakeword, wakeword_label, _levenshtein_distance, _fuzzy_match
from rag_pipeline import build_llm_prompt_for_qa, _truncate_to_two_sentences
from translation_service import translate_question_to_en, translate_answer_from_en, translate, LanguageCode

# ─────────────────────────────────────────────
#  언어별 고정 멘트 & 스크립트
# ─────────────────────────────────────────────
PHRASES = {
    "arrived": {
        "ko": "{spot_name}에 도착했습니다.",
        "en": "We have arrived at {spot_name}.",
        "zh": "我们已经到达{spot_name}。",
        "ja": "{spot_name}に到着しました。",
        "fr": "Nous sommes arrivés à {spot_name}.",
        "es": "Hemos llegado a {spot_name}.",
        "vi": "Chúng ta đã đến {spot_name}.",
        "th": "เรามาถึง{spot_name}แล้ว",
    },
    "tour_start_welcome": {
        "ko": "도리 투어에 오신 것을 환영합니다.",
        "en": "Welcome to the Dori tour.",
        "zh": "欢迎参加多里导览。",
        "ja": "ドリツアーへようこそ。",
        "fr": "Bienvenue à la visite guidée Dori.",
        "es": "Bienvenido al tour de Dori.",
        "vi": "Chào mừng đến với tour Dori.",
        "th": "ยินดีต้อนรับสู่ทัวร์ Dori",
    },
    "tour_start_move": {
        "ko": "그럼 이제 첫 번째 장소로 이동하겠습니다.",
        "en": "Let's move to the first spot.",
        "zh": "那么现在让我们前往第一个地点。",
        "ja": "それでは、最初の場所へ移動しましょう。",
        "fr": "Maintenant, allons au premier lieu.",
        "es": "Ahora vamos al primer lugar.",
        "vi": "Bây giờ chúng ta sẽ di chuyển đến địa điểm đầu tiên.",
        "th": "ตอนนี้เราจะไปยังสถานที่แรกกัน",
    },
    "tour_end": {
        "ko": "모든 투어가 끝났습니다. 함께해주셔서 감사합니다!",
        "en": "The tour is finished. Thank you for joining!",
        "zh": "所有导览已结束。感谢您的参与！",
        "ja": "ツアーが終了しました。ご参加ありがとうございました！",
        "fr": "La visite est terminée. Merci de nous avoir rejoints !",
        "es": "El tour ha terminado. ¡Gracias por acompañarnos!",
        "vi": "Tour đã kết thúc. Cảm ơn bạn đã tham gia!",
        "th": "ทัวร์จบแล้ว ขอบคุณที่เข้าร่วมกับเรา!",
    },
    "qa_intro": {
        "ko": "설명이 끝났습니다. 질문이 있으신가요? 있으시면 말씀해주세요. 없으시면 '패스'라고 말해주셔도 좋아요.",
        "en": "That concludes the explanation. Do you have any questions? If not, you can say 'pass'.",
        "zh": "说明已结束。您有什么问题吗？如果有请告诉我。如果没有，您可以说'跳过'。",
        "ja": "説明が終わりました。ご質問はありますか？ある場合はお知らせください。ない場合は「パス」と言っていただいても結構です。",
        "fr": "L'explication est terminée. Avez-vous des questions ? Si oui, dites-le moi. Sinon, vous pouvez dire 'passer'.",
        "es": "Eso concluye la explicación. ¿Tiene alguna pregunta? Si la tiene, dígamelo. Si no, puede decir 'pasar'.",
        "vi": "Phần giải thích đã kết thúc. Bạn có câu hỏi nào không? Nếu có, hãy cho tôi biết. Nếu không, bạn có thể nói 'bỏ qua'.",
        "th": "คำอธิบายจบแล้ว คุณมีคำถามไหม? ถ้ามีกรุณาบอกฉัน ถ้าไม่มีคุณสามารถพูดว่า 'ผ่าน' ได้",
    },
    "qa_silence": {
        "ko": "말씀이 없으셔서 다음 장소로 이동하겠습니다.",
        "en": "No response, so we'll move to the next spot.",
        "zh": "没有回应，我们将前往下一个地点。",
        "ja": "お返事がないので、次の場所へ移動します。",
        "fr": "Pas de réponse, nous allons donc passer au lieu suivant.",
        "es": "Sin respuesta, así que pasaremos al siguiente lugar.",
        "vi": "Không có phản hồi, nên chúng ta sẽ chuyển sang địa điểm tiếp theo.",
        "th": "ไม่มีคำตอบ เราจะไปยังสถานที่ถัดไป",
    },
    "qa_pass": {
        "ko": "알겠습니다. 다음 장소로 이동할게요.",
        "en": "Okay. We will move to the next spot.",
        "zh": "好的。我们将前往下一个地点。",
        "ja": "承知しました。次の場所へ移動します。",
        "fr": "D'accord. Nous allons passer au lieu suivant.",
        "es": "De acuerdo. Pasaremos al siguiente lugar.",
        "vi": "Được rồi. Chúng ta sẽ chuyển sang địa điểm tiếp theo.",
        "th": "เข้าใจแล้ว เราจะไปยังสถานที่ถัดไป",
    },
    "qa_more": {
        "ko": "추가로 궁금하신 점 있으신가요?",
        "en": "Any other questions?",
        "zh": "还有其他问题吗？",
        "ja": "他にご質問はありますか？",
        "fr": "D'autres questions ?",
        "es": "¿Alguna otra pregunta?",
        "vi": "Bạn còn câu hỏi nào khác không?",
        "th": "มีคำถามอื่นอีกไหม?",
    },
    "photo_intro": {
        "ko": "이곳은 사진이 아주 잘 나오는 장소예요. 사진을 찍어드리겠습니다!",
        "en": "This is a great photo spot. I'll take your picture!",
        "zh": "这里是一个绝佳的拍照地点。我来为您拍照！",
        "ja": "ここは写真がとてもよく撮れる場所です。写真を撮らせていただきます！",
        "fr": "C'est un excellent endroit pour prendre des photos. Je vais prendre votre photo !",
        "es": "Este es un gran lugar para fotos. ¡Le tomaré una foto!",
        "vi": "Đây là một địa điểm chụp ảnh tuyệt vời. Tôi sẽ chụp ảnh cho bạn!",
        "th": "ที่นี่เป็นจุดถ่ายภาพที่ดีมาก ฉันจะถ่ายรูปให้คุณ!",
    },
    "photo_positioning": {
        "ko": "경회루가 잘 보이는 위치에 서주시면, 제가 적절한 위치로 이동해서 사진을 찍어드리겠습니다! 사진을 찍을 때는 저를 봐주세요!",
        "en": "If you stand in a spot with a good view of Gyeong-hoe-ru Pavilion, I'll move to take your picture so you're in the right spot! Please look at me when I take your picture!",
        "zh": "如果您站在能看到庆会楼的位置，我会移动到合适的位置为您拍照！拍照时请看着我！",
        "ja": "慶会楼がよく見える場所に立っていただければ、私が適切な位置に移動して写真を撮らせていただきます！写真を撮る時は私を見てください！",
        "fr": "Si vous vous placez à un endroit avec une bonne vue sur le pavillon Gyeong-hoe-ru, je me déplacerai pour prendre votre photo afin que vous soyez au bon endroit ! Regardez-moi quand je prends votre photo !",
        "es": "Si se coloca en un lugar con buena vista del pabellón Gyeong-hoe-ru, me moveré para tomar su foto para que esté en el lugar correcto. ¡Por favor, míreme cuando tome su foto!",
        "vi": "Nếu bạn đứng ở vị trí có thể nhìn thấy Gyeong-hoe-ru Pavilion rõ ràng, tôi sẽ di chuyển đến vị trí phù hợp để chụp ảnh cho bạn! Khi chụp ảnh, hãy nhìn vào tôi!",
        "th": "หากคุณยืนในตำแหน่งที่มองเห็นเกียงเฮรูได้ดี ฉันจะเคลื่อนที่ไปถ่ายรูปให้คุณในตำแหน่งที่เหมาะสม! กรุณามองมาที่ฉันเมื่อฉันถ่ายรูป!",
    },
    "photo_countdown": {
        "ko": "5초 뒤에 사진을 찍겠습니다! 웃어주세요~",
        "en": "I'll take your picture in five seconds! Smile~",
        "zh": "五秒后我将为您拍照！请微笑~",
        "ja": "5秒後に写真を撮ります！笑顔で~",
        "fr": "Je vais prendre votre photo dans cinq secondes ! Souriez~",
        "es": "¡Le tomaré una foto en cinco segundos! Sonría~",
        "vi": "Tôi sẽ chụp ảnh trong năm giây nữa! Hãy cười lên~",
        "th": "ฉันจะถ่ายรูปในอีก 5 วินาที! ยิ้มหน่อย~",
    },
    "photo_shot": {
        "ko": "찰칵!",
        "en": "Click!",
        "zh": "咔嚓！",
        "ja": "カシャ！",
        "fr": "Clac !",
        "es": "¡Click!",
        "vi": "Cạch!",
        "th": "แชะ!",
    },
    "photo_saved": {
        "ko": "사진이 저장되었습니다! 나중에 받아가실 수 있어요.",
        "en": "Photo saved! You can get it later.",
        "zh": "照片已保存！您稍后可以获取。",
        "ja": "写真が保存されました！後で受け取ることができます。",
        "fr": "Photo enregistrée ! Vous pourrez la récupérer plus tard.",
        "es": "¡Foto guardada! Puede obtenerla más tarde.",
        "vi": "Ảnh đã được lưu! Bạn có thể lấy sau.",
        "th": "บันทึกรูปภาพแล้ว! คุณสามารถรับได้ภายหลัง",
    },
}


# 간단한 spot 설명 스크립트 (하드코딩, 다국어 지원)
SPOT_SCRIPTS = {
    "ko": {
        "gwanghwamun": [
            "광화문은 경복궁의 정문으로, 조선 왕조의 위엄을 상징합니다.",
            "임진왜란과 한국전쟁을 거치며 여러 차례 훼손과 복원을 반복했습니다.",
        ],
        "heungnyemun": [
            "흥례문은 광화문을 지나 경복궁으로 들어오는 두 번째 문입니다.",
            "왕실 의식이 진행될 때 신하들이 대기하던 공간과 맞닿아 있습니다.",
        ],
        "geunjeongmun": [
            "근정문은 근정전 앞마당으로 들어가는 문으로, 공식 조회의 입구였습니다.",
        ],
        "geunjeongjeon": [
            "근정전은 국왕이 정사를 보던 정전으로, 경복궁의 중심 건물입니다.",
            "이곳에서 즉위식과 외국 사신 접견 같은 국가 의례가 열렸습니다.",
        ],
        "sujeongjeon": [
            "수정전은 왕과 신하들이 학문과 정치에 대해 토론하던 장소였습니다.",
        ],
        "gyeonghoeru": [
            "경회루는 연못 위에 세워진 누각으로, 연회와 외국 사신 접대를 위해 사용되었습니다.",
        ],
    },
    "en": {
        "gwanghwamun": [
            "Gwang-wha-mun is the main gate of Gyeong-bok-gung Palace, symbolizing the authority of the Joseon dynasty.",
            "It was damaged and restored multiple times through the Imjin War and the Korean War.",
        ],
        "heungnyemun": [
            "Heung-nye-mun is the second gate after Gwang-wha-mun when entering Gyeong-bok-gung.",
            "It connects to spaces where officials waited during royal ceremonies.",
        ],
        "geunjeongmun": [
            "Geun-jeong-mun is the gate leading to the main courtyard of Geun-jeong-jeon, used for official audiences.",
        ],
        "geunjeongjeon": [
            "Geun-jeong-jeon is the main throne hall where the king handled state affairs.",
            "Coronations and receptions for foreign envoys took place here.",
        ],
        "sujeongjeon": [
            "Su-jeong-jeon was a hall where the king and officials discussed studies and politics.",
        ],
        "gyeonghoeru": [
            "Gyeong-hoe-ru is a pavilion built over a pond, used for banquets and receptions of foreign envoys.",
        ],
    },
    "zh": {
        "gwanghwamun": [
            "光化门是景福宫的正门，象征着朝鲜王朝的威严。",
            "经过壬辰倭乱和韩国战争，多次遭到破坏和修复。",
        ],
        "heungnyemun": [
            "兴礼门是经过光化门进入景福宫的第二道门。",
            "它与王室仪式进行时大臣们等待的空间相连。",
        ],
        "geunjeongmun": [
            "勤政门是通往勤政殿前院的门，是正式朝会的入口。",
        ],
        "geunjeongjeon": [
            "勤政殿是国王处理政务的正殿，是景福宫的中心建筑。",
            "即位仪式和接见外国使节等国家典礼在这里举行。",
        ],
        "sujeongjeon": [
            "修政殿是国王和大臣们讨论学问和政治的场所。",
        ],
        "gyeonghoeru": [
            "庆会楼是建在池塘上的楼阁，用于宴会和接待外国使节。",
        ],
    },
    "ja": {
        "gwanghwamun": [
            "光化門は景福宮の正門で、朝鮮王朝の威厳を象徴しています。",
            "壬辰倭乱と朝鮮戦争を経て、何度も破壊と復元を繰り返しました。",
        ],
        "heungnyemun": [
            "興礼門は光化門を過ぎて景福宮に入る二番目の門です。",
            "王室儀式が行われる際、臣下たちが待機していた空間と接しています。",
        ],
        "geunjeongmun": [
            "勤政門は勤政殿の前庭に入る門で、公式朝会の入口でした。",
        ],
        "geunjeongjeon": [
            "勤政殿は国王が政務を見た正殿で、景福宮の中心建物です。",
            "ここで即位式や外国使節の接見などの国家儀式が行われました。",
        ],
        "sujeongjeon": [
            "修政殿は王と臣下が学問と政治について議論した場所でした。",
        ],
        "gyeonghoeru": [
            "慶会楼は池の上に建てられた楼閣で、宴会や外国使節の接待に使用されました。",
        ],
    },
    "fr": {
        "gwanghwamun": [
            "Gwang-hwa-mun est la porte principale du palais Gyeong-bok-gung, symbolisant l'autorité de la dynastie Joseon.",
            "Elle a été endommagée et restaurée plusieurs fois pendant la guerre d'Imjin et la guerre de Corée.",
        ],
        "heungnyemun": [
            "Heung-nye-mun est la deuxième porte après Gwang-hwa-mun en entrant dans Gyeong-bok-gung.",
            "Elle est reliée aux espaces où les fonctionnaires attendaient pendant les cérémonies royales.",
        ],
        "geunjeongmun": [
            "Geun-jeong-mun est la porte menant à la cour principale de Geun-jeong-jeon, utilisée pour les audiences officielles.",
        ],
        "geunjeongjeon": [
            "Geun-jeong-jeon est la salle du trône principale où le roi gérait les affaires de l'État.",
            "Les couronnements et les réceptions d'envoyés étrangers se déroulaient ici.",
        ],
        "sujeongjeon": [
            "Su-jeong-jeon était une salle où le roi et les fonctionnaires discutaient d'études et de politique.",
        ],
        "gyeonghoeru": [
            "Gyeong-hoe-ru est un pavillon construit sur un étang, utilisé pour les banquets et les réceptions d'envoyés étrangers.",
        ],
    },
    "es": {
        "gwanghwamun": [
            "Gwang-hwa-mun es la puerta principal del palacio Gyeong-bok-gung, que simboliza la autoridad de la dinastía Joseon.",
            "Fue dañada y restaurada múltiples veces durante la guerra de Imjin y la guerra de Corea.",
        ],
        "heungnyemun": [
            "Heung-nye-mun es la segunda puerta después de Gwang-hwa-mun al entrar en Gyeong-bok-gung.",
            "Se conecta con los espacios donde los funcionarios esperaban durante las ceremonias reales.",
        ],
        "geunjeongmun": [
            "Geun-jeong-mun es la puerta que conduce al patio principal de Geun-jeong-jeon, utilizada para audiencias oficiales.",
        ],
        "geunjeongjeon": [
            "Geun-jeong-jeon es el salón del trono principal donde el rey manejaba los asuntos del estado.",
            "Las coronaciones y las recepciones de enviados extranjeros tuvieron lugar aquí.",
        ],
        "sujeongjeon": [
            "Su-jeong-jeon era un salón donde el rey y los funcionarios discutían estudios y política.",
        ],
        "gyeonghoeru": [
            "Gyeong-hoe-ru es un pabellón construido sobre un estanque, utilizado para banquetes y recepciones de enviados extranjeros.",
        ],
    },
    "vi": {
        "gwanghwamun": [
            "Gwang-hwa-mun là cổng chính của cung điện Gyeong-bok-gung, tượng trưng cho quyền uy của triều đại Joseon.",
            "Nó đã bị hư hại và được phục hồi nhiều lần qua cuộc chiến Imjin và Chiến tranh Triều Tiên.",
        ],
        "heungnyemun": [
            "Heung-nye-mun là cổng thứ hai sau Gwang-hwa-mun khi vào Gyeong-bok-gung.",
            "Nó kết nối với các không gian nơi các quan chức chờ đợi trong các nghi lễ hoàng gia.",
        ],
        "geunjeongmun": [
            "Geun-jeong-mun là cổng dẫn đến sân chính của Geun-jeong-jeon, được sử dụng cho các buổi yết kiến chính thức.",
        ],
        "geunjeongjeon": [
            "Geun-jeong-jeon là điện chính nơi nhà vua xử lý các vấn đề quốc gia.",
            "Lễ đăng quang và tiếp đón sứ giả nước ngoài diễn ra tại đây.",
        ],
        "sujeongjeon": [
            "Su-jeong-jeon là một điện nơi nhà vua và các quan chức thảo luận về học vấn và chính trị.",
        ],
        "gyeonghoeru": [
            "Gyeong-hoe-ru là một lầu được xây dựng trên ao, được sử dụng cho các bữa tiệc và tiếp đón sứ giả nước ngoài.",
        ],
    },
    "th": {
        "gwanghwamun": [
            "ควังฮวามุนเป็นประตูหลักของพระราชวังคยองบกกุง สัญลักษณ์แห่งอำนาจของราชวงศ์โชซอน",
            "มันถูกทำลายและบูรณะหลายครั้งผ่านสงครามอิมจินและสงครามเกาหลี",
        ],
        "heungnyemun": [
            "ฮึงเยมุนเป็นประตูที่สองหลังจากควังฮวามุนเมื่อเข้าสู่คยองบกกุง",
            "มันเชื่อมต่อกับพื้นที่ที่ขุนนางรอคอยระหว่างพิธีกรรมของราชวงศ์",
        ],
        "geunjeongmun": [
            "คึนจองมุนเป็นประตูที่นำไปสู่ลานหน้าของคึนจองจอน ใช้สำหรับการเข้าเฝ้าอย่างเป็นทางการ",
        ],
        "geunjeongjeon": [
            "คึนจองจอนเป็นท้องพระโรงหลักที่กษัตริย์จัดการกิจการของรัฐ",
            "พิธีราชาภิเษกและการต้อนรับทูตต่างประเทศเกิดขึ้นที่นี่",
        ],
        "sujeongjeon": [
            "ซูจองจอนเป็นห้องที่กษัตริย์และขุนนางหารือเกี่ยวกับการศึกษาและการเมือง",
        ],
        "gyeonghoeru": [
            "คยองเฮรูเป็นศาลาที่สร้างเหนือสระน้ำ ใช้สำหรับงานเลี้ยงและการต้อนรับทูตต่างประเทศ",
        ],
    },
}


# ===========================================================
# 1) 스팟 스크립트 읽기
# ===========================================================
def run_spot_intro(spot_code, lang):
    """
    spot_code에 해당하는 설명 스크립트를 하드코딩된 SPOT_SCRIPTS에서 가져와 TTS로 읽는다.
    """
    # 하드코딩된 스크립트 사용 (언어별로 직접 제공)
    scripts = SPOT_SCRIPTS.get(lang, {}).get(spot_code) or SPOT_SCRIPTS["en"].get(spot_code, [])
    
    for text in scripts:
        speak(text, lang)
        time.sleep(0.3)
        if _check_wakeword_inline(lang):
            _handle_inline_question(spot_code, lang)
        time.sleep(0.2)


# ===========================================================
# Proper noun normalization for Gyeongbokgung Palace
# ===========================================================
# Palace-related proper nouns with common variations
PALACE_PROPER_NOUNS = {
    "gwanghwamun": ["gwanghwamun", "gwanghwa mun", "gwang hwa mun", "kwanghwamun", "kwanghwa mun"],
    "heungnyemun": ["heungnyemun", "heung nye mun", "heungnye mun", "hungnyemun", "hung nye mun"],
    "geunjeongmun": ["geunjeongmun", "geun jeong mun", "geunjeong mun", "keunjeongmun", "keun jeong mun"],
    "geunjeongjeon": ["geunjeongjeon", "geun jeong jeon", "geunjeong jeon", "keunjeongjeon", "keun jeong jeon"],
    "sujeongjeon": ["sujeongjeon", "su jeong jeon", "sujeong jeon", "sujeongjeon", "su jeong jeon"],
    "gyeonghoeru": ["gyeonghoeru", "gyeong hoe ru", "gyeonghoe ru", "kyeonghoeru", "kyeong hoe ru"],
    "gyeongbokgung": ["gyeongbokgung", "gyeongbok gung", "gyeong bok gung", "kyeongbokgung", "kyeongbok gung"],
}


def _normalize_palace_proper_nouns(text: str, lang: str) -> str:
    """
    Normalize mispronounced palace proper nouns in the question text.
    Uses fuzzy matching to recognize similar pronunciations.
    """
    normalized_text = text
    text_lower = text.lower()
    
    # For each proper noun, check if any variation appears in the text
    for correct_name, variations in PALACE_PROPER_NOUNS.items():
        # Check for exact matches first (most common case)
        for variation in variations:
            if variation in text_lower:
                # Replace with correct name (case-insensitive)
                pattern = re.compile(re.escape(variation), re.IGNORECASE)
                normalized_text = pattern.sub(correct_name, normalized_text)
                if variation != correct_name:
                    print(f"🔍 Matched '{variation}' → '{correct_name}'")
                break
        else:
            # If no exact match, try fuzzy matching on words
            words = re.findall(r'\b\w+\b', text_lower)
            for word in words:
                # Check if this word is similar to any variation
                for variation in variations:
                    # Only check words of similar length
                    if abs(len(word) - len(variation)) <= 2 and len(word) >= 4:
                        distance = _levenshtein_distance(word, variation)
                        if distance <= 2:
                            # Replace the word with correct name
                            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                            normalized_text = pattern.sub(correct_name, normalized_text)
                            print(f"🔍 Fuzzy matched '{word}' → '{correct_name}' (distance: {distance})")
                            break
    
    return normalized_text


# ===========================================================
# 2) 스팟 Q&A 세션
# ===========================================================
def run_qa_session(spot_code, lang):
    """
    질문 → RAG → LLM → TTS
    - 질문이 없거나 '패스' 계열 → 자동 이동
    - 질문 있으면 답변하고 "추가 질문 있으신가요?" 반복
    
    Note:
    - lang은 wakeword 감지 시 결정된 사용자 언어를 사용
    - STT는 해당 언어로만 인식 (자동 언어 감지 없음)
    - RAG 오류 발생 시 자동으로 LLM-only 모드로 전환
    """
    # Special intro for geunjeongjeon (covers both geunjeongmun and geunjeongjeon)
    if spot_code == "geunjeongjeon":
        if lang == "ko":
            intro_text = "Geunjeongmun과 Geunjeongjeon에 대한 설명이 끝났습니다. 질문이 있으신가요? 있으시면 말씀해주세요. 없으시면 '패스'라고 말해주셔도 좋아요."
        elif lang == "en":
            intro_text = "That concludes the explanation of Geun-jeong-mun and Geun-jeong-jeon. Do you have any questions? If not, you can say 'pass'."
        elif lang == "zh":
            intro_text = "关于勤政门和勤政殿的说明已结束。您有什么问题吗？如果有请告诉我。如果没有，您可以说'跳过'。"
        elif lang == "ja":
            intro_text = "勤政門と勤政殿の説明が終わりました。ご質問はありますか？ある場合はお知らせください。ない場合は「パス」と言っていただいても結構です。"
        elif lang == "fr":
            intro_text = "L'explication de Geun-jeong-mun et Geun-jeong-jeon est terminée. Avez-vous des questions ? Si oui, dites-le moi. Sinon, vous pouvez dire 'passer'."
        elif lang == "es":
            intro_text = "Eso concluye la explicación de Geun-jeong-mun y Geun-jeong-jeon. ¿Tiene alguna pregunta? Si la tiene, dígamelo. Si no, puede decir 'pasar'."
        elif lang == "vi":
            intro_text = "Phần giải thích về Geun-jeong-mun và Geun-jeong-jeon đã kết thúc. Bạn có câu hỏi nào không? Nếu có, hãy cho tôi biết. Nếu không, bạn có thể nói 'bỏ qua'."
        elif lang == "th":
            intro_text = "คำอธิบายเกี่ยวกับคึนจองมุนและคึนจองจอนจบแล้ว คุณมีคำถามไหม? ถ้ามีกรุณาบอกฉัน ถ้าไม่มีคุณสามารถพูดว่า 'ผ่าน' ได้"
        else:
            intro_text = "That concludes the explanation of Geun-jeong-mun and Geun-jeong-jeon. Do you have any questions? If not, you can say 'pass'."
        speak(intro_text, lang)
    else:
        speak(PHRASES["qa_intro"][lang], lang)

    while True:
        print("🎙 STT 대기중... (최대 10초)")
        user_text = listen_for_seconds(lang=lang, seconds=10)

        # --- 10초 동안 아무 말 없으면 ---
        if not user_text:
            speak(PHRASES["qa_silence"][lang], lang)
            return

        normalized = user_text.lower().strip()

        # --- '패스' 계열 발화 처리 ---
        # Use word boundaries to avoid matching "no" in "know" or "not"
        PASS_WORDS = [
            # Korean
            "패스", "없어", "괜찮아", "없습니다", "아니오",
            # English
            "pass", "no", "skip", "next", "none",
            # Chinese
            "跳过", "没有", "不用", "不需要", "不",
            # Japanese
            "パス", "ない", "いいえ", "スキップ", "なし",
            # French
            "passer", "non", "rien", "suivant", "aucun",
            # Spanish
            "pasar", "no", "nada", "siguiente", "ninguno",
            # Vietnamese
            "bỏ qua", "không", "không có", "tiếp theo", "không cần",
            # Thai
            "ผ่าน", "ไม่มี", "ไม่", "ข้าม", "ไม่ต้อง",
        ]
        # Check for whole words only (word boundaries)
        words_in_text = set(re.findall(r'\b\w+\b', normalized))
        pass_words_set = set(p.lower() for p in PASS_WORDS)
        if words_in_text.intersection(pass_words_set):
            speak(PHRASES["qa_pass"][lang], lang)
            return

        # --- Proper noun normalization for palace-related terms ---
        normalized = _normalize_palace_proper_nouns(normalized, lang)
        if normalized != user_text.lower().strip():
            print(f"📝 Normalized question: '{user_text}' → '{normalized}'")

        # ====================================================================
        # Q&A PROCESSING: RAG + LLM
        # ====================================================================
        # This section handles user questions using RAG (Retrieval-Augmented Generation)
        # RAG can be enabled/disabled via ENABLE_RAG flag in config.py
        # 
        # When ENABLE_RAG = True:  Uses knowledge_docs context for accurate answers
        # When ENABLE_RAG = False: Uses LLM general knowledge only
        # ====================================================================
        print(f"사용자 질문: {normalized}")

        # 질문을 영어로 번역 (RAG는 영어로 작동)
        question_en = translate_question_to_en(normalized, src=lang)
        print(f"[Q&A] Translated to EN → '{question_en}'")

        # RAG 컨텍스트를 포함한 프롬프트 생성
        # Note: build_llm_prompt_for_qa() checks ENABLE_RAG flag internally
        # If RAG is disabled, it will generate a prompt without context
        prompt = build_llm_prompt_for_qa(
            spot_code=spot_code,
            user_question=question_en,
            place_id="gyeongbokgung",
            language="en",  # LLM은 항상 영어로 답변, 이후 번역
        )
        
        # LLM으로 답변 생성 (영어로 답변받음, 짧은 답변 강제)
        answer_en = call_llm(prompt, temperature=0.7, max_tokens=150).strip()
        # 안전장치: 2문장으로 제한
        answer_en = _truncate_to_two_sentences(answer_en)
        print(f"[Q&A] LLM answer (EN) → '{answer_en}'")
        
        # 답변을 사용자 언어로 번역
        answer = translate_answer_from_en(answer_en, tgt=lang)
        print(f"[Q&A] Translated answer ({lang}) → '{answer}'")

        speak(answer, lang)
        time.sleep(0.3)

        # --- 추가 질문 유도 ---
        speak(PHRASES["qa_more"][lang], lang)


# ===========================================================
# 3) 마지막 스팟 — 사진 촬영 모드
# ===========================================================
def run_photo_mode(lang):
    # Automatically proceed with photo taking after explanation
    speak(PHRASES["photo_intro"][lang], lang)
    time.sleep(0.5)
    
    speak(PHRASES["photo_positioning"][lang], lang)
    time.sleep(1.5)
    
    speak(PHRASES["photo_countdown"][lang], lang)
    # Wait 5 seconds before taking the photo
    time.sleep(5.0)
    
    speak(PHRASES["photo_shot"][lang], lang)
    
    # TODO: 실제 카메라 촬영 코드 연결
    # capture_photo()
    
    time.sleep(0.5)
    speak(PHRASES["photo_saved"][lang], lang)


# ===========================================================
# 4) 전체 투어 루프
# ===========================================================
def start_dori_tour(lang="ko"):
    """
    도리의 전체 투어 엔진
    """
    speak(PHRASES["tour_start_welcome"][lang], lang)
    time.sleep(0.3)
    speak(PHRASES["tour_start_move"][lang], lang)
    time.sleep(0.5)

    for spot in TOUR_ROUTE:
        spot_code = spot["spot_code"]
        spot_name = spot.get(f"name_{lang}", spot["name_en"])
        is_photo_spot = spot.get("is_photo_spot", False)

        # 스팟 이름 멘트
        speak(PHRASES["arrived"][lang].format(spot_name=spot_name), lang)

        # 스팟 설명 읽기
        run_spot_intro(spot_code, lang)

        # Q&A: geunjeongmun에서는 건너뛰고, geunjeongjeon에서만 실행 (두 스팟 모두 설명 후)
        if spot_code != "geunjeongmun":
            run_qa_session(spot_code, lang)

        # 사진 스팟이면 사진 모드 실행
        if is_photo_spot:
            run_photo_mode(lang)

    speak(PHRASES["tour_end"][lang], lang)


# ===========================================================
# 5) 인라인 웨이크워드 인터럽트 핸들러
# ===========================================================
def _check_wakeword_inline(lang: str) -> bool:
    """
    짧게 STT를 돌려 웨이크워드가 들렸는지 확인.
    - 2초 청취, 선택된 언어 코드 사용
    """
    text = listen_for_seconds(lang=lang, seconds=2)
    if not text:
        return False
    print(f"[WakeWord-inline] captured: {text}")
    return is_wakeword(text, lang)


def _handle_inline_question(spot_code: str, lang: str):
    """
    웨이크워드로 인터럽트된 경우 한 번의 질문에 답하고 스크립트를 이어감.
    """
    speak(PHRASES["qa_intro"][lang], lang)

    user_text = listen_for_seconds(lang=lang, seconds=6)
    if not user_text:
        speak(PHRASES["qa_silence"][lang], lang)
        return

    normalized = user_text.lower().strip()
    
    # --- Proper noun normalization for palace-related terms ---
    normalized = _normalize_palace_proper_nouns(normalized, lang)
    if normalized != user_text.lower().strip():
        print(f"📝 Normalized question: '{user_text}' → '{normalized}'")
    
    print(f"[Q&A-inline] question: {normalized}")

    # 질문을 영어로 번역 (RAG는 영어로 작동)
    question_en = translate_question_to_en(normalized, src=lang)
    
    # RAG 컨텍스트를 포함한 프롬프트 생성
    # Note: RAG toggle (ENABLE_RAG in config.py) is checked inside build_llm_prompt_for_qa()
    prompt = build_llm_prompt_for_qa(
        spot_code=spot_code,
        user_question=question_en,
        place_id="gyeongbokgung",
        language="en",  # LLM은 항상 영어로 답변, 이후 번역
    )
    
    # LLM으로 답변 생성 (짧은 답변 강제)
    answer_en = call_llm(prompt, temperature=0.7, max_tokens=150).strip()
    # 안전장치: 2문장으로 제한
    answer_en = _truncate_to_two_sentences(answer_en)
    
    # 답변을 사용자 언어로 번역
    answer = translate_answer_from_en(answer_en, tgt=lang)
    speak(answer, lang)

    # 안내 멘트 후 스크립트로 복귀
    speak(PHRASES["qa_more"][lang], lang)


# 별칭: 기존 코드 호환
def run_tour(user_lang="ko", place_id="gyeongbokgung", qa_record_seconds=10.0, max_qa_turns=3):
    """
    Wrapper for legacy import compatibility.
    """
    return start_dori_tour(lang=user_lang)
