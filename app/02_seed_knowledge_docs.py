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
        # General Gyeongbokgung Palace information from QA document
        {
            "text": (
                "Meaning 'May the new dynasty enjoy great fortune and prosperity,' Gyeongbokgung Palace was the main royal palace (beopgung) of the Joseon Dynasty. "
                "It was the first palace built after the founding of Joseon in 1392, following the relocation of the capital to Hanyang in 1394. "
                "Construction was completed in 1395 (the 4th year of King Taejo)."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:overview",
            "tags": ["overview", "history", "founding", "king taejo"],
        },
        {
            "text": (
                "When Gyeongbokgung was built, the palace buildings were laid out in strict formality along a straight central axis. "
                "Starting from the main gate, Gwanghwamun, the sequence of major buildings was Heungnyemun, Geunjeongmun, Geunjeongjeon, Sajeongjeon, Gangnyeongjeon, and Gyotaejeon."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:layout",
            "tags": ["architecture", "layout", "structure"],
        },
        {
            "text": (
                "During the early Joseon period, kings such as Sejong, Seongjong, and Jungjong ascended the throne at Gyeongbokgung. "
                "It was also during King Sejong's reign that Hunminjeongeum, the Korean alphabet, was created."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:early_joseon",
            "tags": ["history", "kings", "hunminjeongeum", "king sejong"],
        },
        {
            "text": (
                "In 1592 (the 25th year of King Seonjo), all palaces in Hanyang, including Gyeongbokgung, were destroyed by fire during the Imjin War. "
                "After being burned down, the palace site remained empty for approximately 270 years."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:imjin_war",
            "tags": ["imjin war", "destruction", "history", "king seonjo"],
        },
        {
            "text": (
                "Reconstruction of the palace began in 1865 (the 2nd year of King Gojong) and was completed in 1867 (the 4th year of King Gojong). "
                "Later, structures such as Hyangwonjeong Pavilion, Jibokjae, and Geoncheonggung were built in the northern area of the palace, "
                "forming the layout of Gyeongbokgung as it is known today."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:reconstruction",
            "tags": ["reconstruction", "king gojong", "history", "architecture"],
        },
        {
            "text": (
                "After the Japan–Korea Annexation Treaty in 1910, Gyeongbokgung was systematically damaged by the Japanese colonial government. "
                "From 1911, it came under the management of the Japanese Government-General of Korea, and from 1915 onward, more than 90% of the palace buildings—except for a few major structures—were demolished. "
                "In 1926, the Government-General building was constructed on the palace grounds, causing Gyeongbokgung to lose its dignity as a royal palace."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:colonial_period",
            "tags": ["colonial period", "japanese occupation", "demolition", "history"],
        },
        {
            "text": (
                "Full-scale restoration efforts began in the 1990s. Although the palace was opened to the public in the 1960s, proper restoration was delayed for over 30 years "
                "because the area behind the palace was occupied by the Blue House (Cheong Wa Dae) and military facilities responsible for its defense."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:restoration_1990s",
            "tags": ["restoration", "cheong wa dae", "history"],
        },
        {
            "text": (
                "During the Korean War, Gwanghwamun Gate was reduced to its framework by bombing and was later reconstructed in concrete in the 1960s. "
                "Restoration efforts during this period were only partial and fragmentary."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:korean_war",
            "tags": ["korean war", "gwanghwamun", "restoration", "history"],
        },
        {
            "text": (
                "After the introduction of direct presidential elections in 1987, policies were implemented to return areas and facilities occupied by the military and government to the public. "
                "This marked the beginning of a long-term restoration project for Gyeongbokgung."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:restoration_project",
            "tags": ["restoration", "history", "policy"],
        },
        {
            "text": (
                "In 1990, the government launched the first phase of a 20-year restoration plan. In 1995, marking the 50th anniversary of liberation, "
                "the Japanese Government-General building that had blocked the front of Gyeongbokgung was finally demolished. "
                "The first phase of restoration was completed in 2010, during which 89 buildings covering 8,987㎡ (approximately 2,720 pyeong) were restored."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:restoration_phase1",
            "tags": ["restoration", "government-general building", "history"],
        },
        {
            "text": (
                "Including 36 buildings that survived the Japanese colonial period, a total of 125 buildings now stand within the palace grounds, "
                "reaching about 25% of the scale of Gyeongbokgung during King Gojong's reign. Since September 2010, the Gwanghwamun area has been fully opened to the public."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:current_status",
            "tags": ["restoration", "statistics", "current status"],
        },
        {
            "text": (
                "The second phase of restoration began in 2011 and consists of both maintenance and long-term reconstruction projects. "
                "The goal is to restore the palace to approximately 75% of its size during King Gojong's era by 2030."
            ),
            "source_type": "extra",
            "source_ref": "qa:gyeongbokgung:restoration_phase2",
            "tags": ["restoration", "future plans", "2030"],
        },
        # FAQ entries
        {
            "text": (
                "After founding the Joseon Dynasty, King Taejo's first priorities were to build Jongmyo Shrine to honor royal ancestors and a palace where the royal family and government officials could reside. "
                "Construction of the palace took about ten months. After surveying the land, construction began in December 1394 (the 3rd year of King Taejo) and was completed in September of the following year. "
                "The palace included spaces for state affairs, royal residence, officials' offices, walls, and gates, and it was named 'Gyeongbokgung.'"
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:construction_time",
            "tags": ["faq", "construction", "king taejo", "history"],
        },
        {
            "text": (
                "Both Gyeongbokgung and the Forbidden City in China have a rectangular layout with important buildings aligned from south to north. "
                "However, the Forbidden City is wider and shallower, while Gyeongbokgung is narrower but much deeper. "
                "The Forbidden City is surrounded by a wide moat for defense, whereas Gyeongbokgung does not have such a water barrier. "
                "Another difference is geography: the Forbidden City is built on flat land with an artificial hill behind it, "
                "while Gyeongbokgung lies at the foot of Mt. Baekak (Bugaksan), using natural terrain as a defensive feature."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:forbidden_city_comparison",
            "tags": ["faq", "comparison", "architecture", "forbidden city"],
        },
        {
            "text": (
                "The area where Cheong Wa Dae stands today was once the palace's rear garden. "
                "During the Japanese colonial period, the Japanese built the governor-general's residence there to suppress Korea's national spirit. "
                "After liberation, the site became the presidential residence."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:cheong_wa_dae",
            "tags": ["faq", "cheong wa dae", "history", "colonial period"],
        },
        {
            "text": (
                "If Dae Jang-geum had worked as a cook in the palace, she would have done so in the Suragan, where all palace food was prepared. "
                "The Suragan included facilities such as Saenggwabang and Sojubang. "
                "Historically, Dae Jang-geum was actually a female physician (uinyeo) during King Jungjong's reign, and records do not confirm her role as a royal cook, which was dramatized in TV series."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:dae_jang_geum",
            "tags": ["faq", "dae jang-geum", "history", "cooking", "king jungjong"],
        },
        {
            "text": (
                "Empress Myeongseong was assassinated by Japanese agents at Gonryeonghap Hall in Geoncheonggung, north of Hyangwonjeong Pavilion, in 1895."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:empress_myeongseong",
            "tags": ["faq", "empress myeongseong", "assassination", "history", "geoncheonggung"],
        },
        {
            "text": (
                "A bronze dragon was discovered in 1997 during cleaning of Gyeonghoeru Pond. "
                "It was placed there to prevent fire, as dragons were believed to control water and rain."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:gyeonghoeru_dragon",
            "tags": ["faq", "gyeonghoeru", "dragon", "symbolism"],
        },
        {
            "text": (
                "A king's day involved greeting elders, meeting officials, discussing state affairs, studying Confucianism and history, "
                "and overseeing palace security, often continuing late into the night."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:king_daily_routine",
            "tags": ["faq", "king", "daily life", "routine"],
        },
        {
            "text": (
                "Although exact numbers are unknown, it is estimated that around 3,000 people lived or worked in Gyeongbokgung during the Joseon Dynasty, "
                "including royal family members, officials, palace women, eunuchs, soldiers, cooks, and physicians."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:palace_population",
            "tags": ["faq", "population", "joseon dynasty", "statistics"],
        },
        {
            "text": (
                "Nets installed under the eaves of large palace buildings are called busi. "
                "They prevent birds from nesting under the eaves, which could soil and damage the elaborately painted wooden structures."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:busi_nets",
            "tags": ["faq", "architecture", "busi", "preservation"],
        },
        {
            "text": (
                "During the Japanese colonial period, the palace was used for exhibitions and fairs, during which many buildings were damaged or dismantled, "
                "turning the palace into a public park."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:colonial_exhibitions",
            "tags": ["faq", "colonial period", "exhibitions", "history"],
        },
        {
            "text": (
                "When a king passed away, the king's body was placed in a temporary hall, followed by a royal funeral and three years of mourning. "
                "Afterward, the spirit tablet was enshrined at Jongmyo Shrine."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:king_funeral",
            "tags": ["faq", "funeral", "jongmyo", "ritual"],
        },
        {
            "text": (
                "Films and dramas have been shot at Gyeongbokgung, including The King and I (2008), Deep Rooted Tree (2011), Masquerade (2012), and others. "
                "However, most palace scenes are filmed on sets to protect the site."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:films_dramas",
            "tags": ["faq", "films", "dramas", "entertainment"],
        },
        {
            "text": (
                "Dae Jang-geum was a real female physician, though her role as a royal cook is fictional."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:dae_jang_geum_real",
            "tags": ["faq", "dae jang-geum", "history"],
        },
        {
            "text": (
                "Among 32 queens with known birth and death dates, the average lifespan of Joseon queens was approximately 47.5 years."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:queen_lifespan",
            "tags": ["faq", "queens", "statistics", "lifespan"],
        },
        {
            "text": (
                "Although regulations existed, many kings exceeded them. Kings Seongjong and Jungjong each had three queens and nine concubines."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:concubines",
            "tags": ["faq", "concubines", "kings", "history"],
        },
        {
            "text": (
                "Historical records indicate that Gyeongbokgung was not burned by Koreans before the Japanese invasion but was later destroyed during the Imjin War."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:palace_burned",
            "tags": ["faq", "imjin war", "destruction", "history"],
        },
        {
            "text": (
                "During the assassination of Empress Myeongseong, King Gojong was confined in Jangandang Hall within Geoncheonggung."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:king_gojong_assassination",
            "tags": ["faq", "king gojong", "empress myeongseong", "assassination"],
        },
        {
            "text": (
                "Ondol (underfloor heating) systems date back to the Goguryeo period and became widespread during the Goryeo and early Joseon periods."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:ondol",
            "tags": ["faq", "ondol", "heating", "architecture", "history"],
        },
        {
            "text": (
                "The name 'Gyeongbokgung' comes from a verse in the Book of Songs, meaning 'May you enjoy great and everlasting fortune,' "
                "expressing hopes for the prosperity of the new dynasty."
            ),
            "source_type": "extra",
            "source_ref": "qa:faq:gyeongbokgung_meaning",
            "tags": ["faq", "meaning", "name", "etymology"],
        },
        # Historical timeline entries
        {
            "text": (
                "In 1446 (the 28th year of King Sejong), Hunminjeongeum, the Korean alphabet, was proclaimed."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1446",
            "tags": ["timeline", "hunminjeongeum", "king sejong"],
        },
        {
            "text": (
                "In 1475 (the 6th year of King Seongjong), the northern gate was named Sinmumun."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1475",
            "tags": ["timeline", "king seongjong", "naming"],
        },
        {
            "text": (
                "In 1873 (the 10th year of King Gojong), Geoncheonggung was constructed."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1873",
            "tags": ["timeline", "king gojong", "geoncheonggung", "construction"],
        },
        {
            "text": (
                "In 1895 (the 32nd year of King Gojong), Empress Myeongseong was assassinated at Okhoru Pavilion in Geoncheonggung."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1895",
            "tags": ["timeline", "empress myeongseong", "assassination", "king gojong"],
        },
        {
            "text": (
                "In 1896 (the 33rd year of King Gojong), King Gojong moved his residence to the Russian Legation."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1896",
            "tags": ["timeline", "king gojong", "russian legation"],
        },
        {
            "text": (
                "In 1915, palace buildings were demolished for the Joseon Industrial Exhibition."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1915",
            "tags": ["timeline", "demolition", "colonial period", "exhibition"],
        },
        {
            "text": (
                "In 1926, the Japanese Government-General building was constructed on the palace grounds."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1926",
            "tags": ["timeline", "government-general building", "colonial period"],
        },
        {
            "text": (
                "From 1990, restoration work began at Gyeongbokgung Palace."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1990",
            "tags": ["timeline", "restoration", "1990s"],
        },
        {
            "text": (
                "From 1994 onward, restoration of the Gangnyeongjeon and Gyotaejeon areas took place."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1994",
            "tags": ["timeline", "restoration", "gangnyeongjeon", "gyotaejeon"],
        },
        {
            "text": (
                "From 1995 to 1997, the Government-General building was demolished."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1995_1997",
            "tags": ["timeline", "demolition", "government-general building"],
        },
        {
            "text": (
                "From 2001 to 2021, restoration of the Heungnyemun area, Gwanghwamun area, Heungbokjeon, Chwihyanggyo Bridge, and repair of Hyangwonjeong took place."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:2001_2021",
            "tags": ["timeline", "restoration", "heungnyemun", "gwanghwamun"],
        },
        {
            "text": (
                "In 2023, restoration of Gyejodang Hall in the Eastern Palace (Donggung) was completed."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:2023",
            "tags": ["timeline", "restoration", "gyejodang", "donggung"],
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
    ],
    # Historical timeline entries
    "gwanghwamun": [
        {
            "text": (
                "In 1426 (the 8th year of King Sejong), Gwanghwamun, Geonchunmun, and Yeongchumun Gates were constructed."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1426",
            "tags": ["timeline", "king sejong", "construction"],
        },
        {
            "text": (
                "In 1446 (the 28th year of King Sejong), Hunminjeongeum, the Korean alphabet, was proclaimed."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1446",
            "tags": ["timeline", "hunminjeongeum", "king sejong"],
        },
        {
            "text": (
                "In 1475 (the 6th year of King Seongjong), the northern gate was named Sinmumun."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1475",
            "tags": ["timeline", "king seongjong", "naming"],
        },
        {
            "text": (
                "In 1873 (the 10th year of King Gojong), Geoncheonggung was constructed."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1873",
            "tags": ["timeline", "king gojong", "geoncheonggung", "construction"],
        },
        {
            "text": (
                "In 1895 (the 32nd year of King Gojong), Empress Myeongseong was assassinated at Okhoru Pavilion in Geoncheonggung."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1895",
            "tags": ["timeline", "empress myeongseong", "assassination", "king gojong"],
        },
        {
            "text": (
                "In 1896 (the 33rd year of King Gojong), King Gojong moved his residence to the Russian Legation."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1896",
            "tags": ["timeline", "king gojong", "russian legation"],
        },
        {
            "text": (
                "In 1915, palace buildings were demolished for the Joseon Industrial Exhibition."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1915",
            "tags": ["timeline", "demolition", "colonial period", "exhibition"],
        },
        {
            "text": (
                "In 1926, the Japanese Government-General building was constructed on the palace grounds."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1926",
            "tags": ["timeline", "government-general building", "colonial period"],
        },
        {
            "text": (
                "From 1990, restoration work began at Gyeongbokgung Palace."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1990",
            "tags": ["timeline", "restoration", "1990s"],
        },
        {
            "text": (
                "From 1994 onward, restoration of the Gangnyeongjeon and Gyotaejeon areas took place."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1994",
            "tags": ["timeline", "restoration", "gangnyeongjeon", "gyotaejeon"],
        },
        {
            "text": (
                "From 1995 to 1997, the Government-General building was demolished."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:1995_1997",
            "tags": ["timeline", "demolition", "government-general building"],
        },
        {
            "text": (
                "From 2001 to 2021, restoration of the Heungnyemun area, Gwanghwamun area, Heungbokjeon, Chwihyanggyo Bridge, and repair of Hyangwonjeong took place."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:2001_2021",
            "tags": ["timeline", "restoration", "heungnyemun", "gwanghwamun"],
        },
        {
            "text": (
                "In 2023, restoration of Gyejodang Hall in the Eastern Palace (Donggung) was completed."
            ),
            "source_type": "extra",
            "source_ref": "qa:timeline:2023",
            "tags": ["timeline", "restoration", "gyejodang", "donggung"],
        },
    ],
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





