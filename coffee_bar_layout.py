# coffee_bar_layout.py

# 0~10 사이 정수 입력 받는 함수
def ask_int_0_10(label):
    while True:
        raw = input(f"{label} (0~10 입력): ")
        try:
            value = int(raw)
        except ValueError:
            print("숫자를 입력해 주세요.")
            continue
        if 0 <= value <= 10:
            return value
        else:
            print("0 이상 10 이하의 숫자만 입력 가능합니다.")

# 동/서/남/북 입력 받는 함수
def ask_direction():
    while True:
        raw = input("주 출입구 위치를 입력해 주세요 (동/서/남/북): ").strip()
        if raw in ("동", "서", "남", "북"):
            return raw
        print("동, 서, 남, 북 중 하나만 정확히 입력해 주세요.")

# 1. 기자재 갯수 입력
def ask_equipments():
    labels = [
        "에스프레소 머신 갯수",
        "에스프레소 그라인더 갯수",
        "에스프레소 정온수기 갯수",
        "기타 음료 정온수기 갯수",
        "브루잉 그라인더 갯수",
        "브루잉 정온수기 갯수",
        "브루잉 포트 갯수",
        "브루잉 드리퍼 갯수",
        "(하부)우유 냉장고 갯수",
        "(하부)서브 냉장고 갯수",
        "(하부)냉장냉동고 갯수",
        "(하부)냉동고 갯수",
        "(하부)제빙기 갯수",
        "냉장 쇼케이스 갯수",
        "상온 쇼케이스 갯수",
        "포스 갯수",
    ]

    counts = {}
    print("=== 기자재 갯수 입력 ===")
    for label in labels:
        counts[label] = ask_int_0_10(label)
    return counts

# 2. 기자재 이름 리스트 생성
def build_equipment_names(counts):
    items = []

    def add_series(prefix, n):
        for i in range(1, n + 1):
            items.append(f"{prefix}{i}")

    add_series("에스프레소 머신", counts["에스프레소 머신 갯수"])
    add_series("에스프레소 그라인더", counts["에스프레소 그라인더 갯수"])
    add_series("에스프레소 정온수기", counts["에스프레소 정온수기 갯수"])
    add_series("기타 음료 정온수기", counts["기타 음료 정온수기 갯수"])
    add_series("브루잉 그라인더", counts["브루잉 그라인더 갯수"])
    add_series("브루잉 정온수기", counts["브루잉 정온수기 갯수"])
    add_series("브루잉 포트", counts["브루잉 포트 갯수"])
    add_series("브루잉 드리퍼", counts["브루잉 드리퍼 갯수"])
    add_series("(하부)우유 냉장고", counts["(하부)우유 냉장고 갯수"])
    add_series("(하부)서브 냉장고", counts["(하부)서브 냉장고 갯수"])
    add_series("(하부)냉장냉동고", counts["(하부)냉장냉동고 갯수"])
    add_series("(하부)냉동고", counts["(하부)냉동고 갯수"])
    add_series("(하부)제빙기", counts["(하부)제빙기 갯수"])
    add_series("냉장 쇼케이스", counts["냉장 쇼케이스 갯수"])
    add_series("상온 쇼케이스", counts["상온 쇼케이스 갯수"])
    add_series("포스", counts["포스 갯수"])

    # 추가 기자재
    items.append("픽업")
    items.append("리턴")
    items.append("싱크볼")

    return items

# 3. 2열 바 구조와 출입구 표시용 텍스트 레이아웃 뼈대 만들기
def init_bar_layout(direction):
    # 전면 바 / 후면 바를 좌우로 두고, 각 바에 여러 슬롯을 둔다.
    # 간단히 10칸씩 예시.
    front = ["[빈]" for _ in range(10)]
    back = ["[빈]" for _ in range(10)]

    # 주 출입구 텍스트
    entrance_text = f"주 출입구({direction})"

    # 설명 편의를 위해 방향만 함께 출력하고,
    # 실제 배치는 전면 바 기준으로 가정.
    return front, back, entrance_text

# 4. 기자재 배치 규칙 적용 (간단 버전)
def place_equipments(front, back, items, direction):
    # 헬퍼 함수들
    def first_empty(bar, prefer_left=True):
        idx_range = range(len(bar)) if prefer_left else reversed(range(len(bar)))
        for i in idx_range:
            if bar[i] == "[빈]":
                return i
        return None

    def find_indices(bar, keyword):
        return [i for i, v in enumerate(bar) if keyword in v]

    # 4-1. 에스프레소 존: 전면 바 가운데 쪽에 배치
    grinders = [i for i in items if i.startswith("에스프레소 그라인더")]
    machines = [i for i in items if i.startswith("에스프레소 머신")]
    boilers = [i for i in items if i.startswith("에스프레소 정온수기")]

    # 최대 한 세트만 우선 배치 (규칙을 단순화)
    if grinders and machines and boilers:
        g = grinders.pop(0)
        m = machines.pop(0)
        b = boilers.pop(0)

        # 주 출입구 방향에 따라 순서 선택
        # 입구 기준 손님 쪽에서 볼 때 그라인더가 먼저 오도록 예시
        center = len(front) // 2
        order1 = [g, m, b]
        order2 = [b, m, g]

        if direction in ("동", "남"):
            order = order1
        else:
            order = order2

        for offset, name in enumerate(order):
            idx = center - 1 + offset
            if 0 <= idx < len(front):
                front[idx] = name

    # 남은 에스프레소 관련 기자재 전면 바 빈칸에 배치
    for name in grinders + machines + boilers:
        idx = first_empty(front)
        if idx is not None:
            front[idx] = name

    # 4-2. 브루잉 관련은 전면 바 빈칸에 채우기
    brewing_items = [i for i in items if "브루잉" in i]
    other_items = [i for i in items if i not in brewing_items]

    for name in brewing_items:
        idx = first_empty(front)
        if idx is not None:
            front[idx] = name
        else:
            # 전면이 꽉 찼으면 후면으로
            idx = first_empty(back)
            if idx is not None:
                back[idx] = name

    # 4-3. 제빙기 + 서브 냉장고: 후면 바 기준으로 함께 배치
    ice_items = [i for i in other_items if "(하부)제빙기" in i]
    sub_fridges = [i for i in other_items if "(하부)서브 냉장고" in i]
    other_items = [i for i in other_items if i not in ice_items + sub_fridges]

    for ice in ice_items:
        idx = first_empty(back)
        if idx is None:
            break
        back[idx] = ice
        # 옆 칸에 서브 냉장고 하나 붙이기
        if sub_fridges:
            neighbor = idx + 1 if idx + 1 < len(back) and back[idx + 1] == "[빈]" else idx - 1
            if 0 <= neighbor < len(back) and back[neighbor] == "[빈]":
                back[neighbor] = sub_fridges.pop(0)

    # 남은 서브 냉장고들 배치
    for s in sub_fridges:
        idx = first_empty(back)
        if idx is not None:
            back[idx] = s

    # 4-4. 우유 냉장고를 에스프레소 머신 근처에
    milk_fridges = [i for i in other_items if "(하부)우유 냉장고" in i]
    other_items = [i for i in other_items if i not in milk_fridges]

    machine_indices = find_indices(front, "에스프레소 머신")
    if machine_indices:
        target_idx = machine_indices[0]
        for milk in milk_fridges:
            # 우측 우선 → 좌측
            placed = False
            for offset in (1, -1, 2, -2):
                idx = target_idx + offset
                if 0 <= idx < len(front) and front[idx] == "[빈]":
                    front[idx] = milk
                    placed = True
                    break
            if not placed:
                idx = first_empty(back)
                if idx is not None:
                    back[idx] = milk
    else:
        for milk in milk_fridges:
            idx = first_empty(front) or first_empty(back)
            if idx is not None:
                (front if idx < len(front) else back)[idx] = milk

    # 4-5. 포스, 픽업, 리턴, 싱크볼 배치
    pos_items = [i for i in other_items if "포스" in i]
    other_items = [i for i in other_items if i not in pos_items]

    pickup = "픽업"
    return_zone = "리턴"
    sink = "싱크볼"

    # 포스는 주 출입구와 가까운 전면 모서리에
    if direction in ("동", "서"):
        idx_pos = 0 if direction == "서" else len(front) - 1
    else:
        # 남/북일 때도 전면 바 기준 왼쪽/오른쪽 선택 (임의)
        idx_pos = 0
    if pos_items:
        front[idx_pos] = pos_items.pop(0)

    # 픽업, 리턴은 전면 바에
    # 포스와 적당히 떨어진 위치에 두되, 리턴과 싱크볼은 가깝게
    # 픽업 먼저 배치
    idx_pickup = first_empty(front, prefer_left=False)
    if idx_pickup is not None:
        front[idx_pickup] = pickup

    # 싱크볼은 주 출입구에서 가장 먼 전면 모서리
    idx_sink = len(front) - 1 if idx_pos == 0 else 0
    # 다른 장비가 있으면 그 옆 빈칸 탐색
    if front[idx_sink] != "[빈]":
        alt = first_empty(front, prefer_left=(idx_sink != 0))
        if alt is not None:
            idx_sink = alt
    front[idx_sink] = sink

    # 리턴은 싱크볼과 최대한 가까운 빈칸
    # 좌우로 한 칸씩 퍼져 나가며 탐색
    for dist in range(1, len(front)):
        left = idx_sink - dist
        right = idx_sink + dist
        placed = False
        if left >= 0 and front[left] == "[빈]":
            front[left] = return_zone
            placed = True
        elif right < len(front) and front[right] == "[빈]":
            front[right] = return_zone
            placed = True
        if placed:
            break

    # 나머지 기자재들을 빈 칸에 채우기
    for name in pos_items + other_items:
        idx = first_empty(front)
        target_bar = front
        if idx is None:
            idx = first_empty(back)
            target_bar = back
        if idx is not None:
            target_bar[idx] = name

    return front, back

# 5. 텍스트로 레이아웃 출력
def print_layout(front, back, entrance_text):
    print("\n=== 커피 바 2열 레이아웃 ===")
    print(f"주 출입구 표시: {entrance_text}")
    print("\n[전면 바]")
    print(" | ".join(front))
    print("\n[후면 바]")
    print(" | ".join(back))

def main():
    counts = ask_equipments()
    direction = ask_direction()

    items = build_equipment_names(counts)

    front, back, entrance_text = init_bar_layout(direction)
    front, back = place_equipments(front, back, items, direction)

    print_layout(front, back, entrance_text)

if __name__ == "__main__":
    main()
