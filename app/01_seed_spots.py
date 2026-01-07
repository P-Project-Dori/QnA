# 01_seed_spots.py

from db_utils import insert_spot
from tour_route import TOUR_ROUTE


def main():
    for spot in TOUR_ROUTE:
        insert_spot(
            code=spot["spot_code"],
            name_en=spot["name_en"],
            order_no=spot["order"],
            lat=None, #GPS
            lng=None, #GPS
            is_photo_spot=spot["is_photo_spot"],
            place_id="gyeongbokgung",  # 추후에 다른 궁궐 추가 시 이런식으로 고정 후 진행
        )
    print("✅ TOUR_ROUTE 기준 spots 데이터 입력 완료!")


if __name__ == "__main__":
    main()
