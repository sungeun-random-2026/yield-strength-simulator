import random
import streamlit as st


# (2) 함수 (def): 힘(N)과 단면적(mm^2)을 받아 응력(MPa)을 계산하는 함수
def calculate_stress(force, area):
    stress = force / area
    return round(stress, 2)


# 1) 시작 및 앱 제목 설정
st.title("🔩 하중 변화에 따른 소재의 응력 분석 웹")
st.caption("재료공학 진로 연계 프로젝트 | 10931 최성은")
st.divider()

# 2) 리스트 선언: 하중 조건, 소재 이름, 각 소재의 항복 강도(MPa)
loads = [500, 1000, 1500, 2000]
material_names = [
    "알루미늄(6061-T6)",
    "스테인리스강(SUS304)",
    "순수 티타늄",
    "구리",
]
yield_strengths = [270, 205, 170, 70]  # 직접 조사하여 검증한 각 소재의 항복 강도(MPa)

# 3) 입력 받기 (UI 레이아웃)
st.subheader("1. 실험 조건 설정")

# random 라이브러리 활용 1: 오늘의 추천 실험 시편 뽑기
if st.button("🎲 랜덤 실험 시편 추천받기"):
    random_idx = random.randint(0, len(material_names) - 1)
    st.info(
        f"오늘의 추천 테스트 소재는 **{material_names[random_idx]}**입니다! 아래 드롭다운에서 선택해 보세요."
    )

# 소재 선택 (드롭다운 목록)
selected_material = st.selectbox("소재 선택:", material_names)

# 단면적 입력 (슬라이더: 1 ~ 20 mm^2)
area = st.slider(
    "시편의 단면적 입력 (mm²):", min_value=1, max_value=20, value=10
)

# random 라이브러리 활용 2: 실제 실험 환경의 미세 오차(±5%) 적용 여부
apply_noise = st.checkbox(
    "실제 실험 오차(랜덤 하중 변동 ±5%) 반영하기", value=False
)

st.divider()

# 4) 버튼 클릭 시 분석 실행
if st.button("🔍 분석하기", type="primary"):
    # 선택한 소재의 인덱스(위치)를 찾아 해당 소재의 항복 강도 가져오기
    idx = material_names.index(selected_material)
    target_yield = yield_strengths[idx]

    st.subheader("2. 결과 출력 화면")
    st.write(
        f"- 선택한 소재(**{selected_material}**)가 영구 변형될 때의 응력(항복 강도): **{target_yield} MPa**"
    )

    # 표(테이블)로 만들기 위해 결과를 담을 빈 리스트 생성
    result_table = []

    # 6) 반복 출력: for문을 이용해 loads 리스트의 모든 하중 조건 계산
    for force in loads:
        if apply_noise:
            actual_force = round(force * random.uniform(0.95, 1.05), 1)
        else:
            actual_force = force

        # 함수 호출로 응력 계산
        stress = calculate_stress(actual_force, area)

        # 5) 조건 판단 (if-elif-else)
        if stress < target_yield * 0.7:
            status = "🟢 안전"
        elif stress < target_yield:
            status = "🟡 주의"
        else:
            status = "🔴 항복(영구변형)"

        result_table.append({
            "적용 하중 (N)": actual_force,
            "계산된 응력 (MPa)": stress,
            "판정": status,
        })

    # 추가 라이브러리 없이 Streamlit 기본 기능만으로 깔끔한 표 출력
    st.table(result_table)
