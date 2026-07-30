import hashlib
from datetime import datetime, timedelta, timezone

import streamlit as st


# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="몽글몽글 오늘의 띠 운세",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).date()
today_text = f"{today.year}년 {today.month}월 {today.day}일"


# ---------------------------------------------------------
# 디자인
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 12% 12%, rgba(255, 215, 231, 0.72), transparent 28%),
                radial-gradient(circle at 88% 15%, rgba(217, 237, 255, 0.82), transparent 28%),
                radial-gradient(circle at 50% 92%, rgba(230, 221, 255, 0.72), transparent 32%),
                linear-gradient(145deg, #fff9fc 0%, #f8fbff 50%, #fffdf6 100%);
        }

        .block-container {
            max-width: 880px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .main-title {
            text-align: center;
            font-size: clamp(2.05rem, 5vw, 3.25rem);
            font-weight: 900;
            color: #5d466b;
            margin-bottom: 0.2rem;
            letter-spacing: -0.04em;
            text-shadow: 0 3px 0 rgba(255, 255, 255, 0.95);
        }

        .sub-title {
            text-align: center;
            color: #8a7294;
            font-size: 1.02rem;
            margin-bottom: 1.5rem;
        }

        .date-badge {
            width: fit-content;
            margin: 0 auto 1.6rem auto;
            padding: 0.48rem 1rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid #eadff0;
            color: #725c7d;
            font-weight: 700;
            box-shadow: 0 8px 24px rgba(96, 72, 110, 0.08);
        }

        .selection-box {
            text-align: center;
            margin: 0.2rem 0 1rem 0;
            padding: 1.15rem;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.76);
            border: 1px solid rgba(231, 217, 239, 0.9);
            box-shadow: 0 12px 30px rgba(98, 75, 111, 0.08);
        }

        .animal-emoji {
            font-size: 4.2rem;
            line-height: 1;
            margin-bottom: 0.4rem;
        }

        .animal-name {
            font-size: 1.5rem;
            color: #5d466b;
            font-weight: 900;
        }

        .animal-caption {
            color: #947c9e;
            margin-top: 0.25rem;
        }

        div[data-testid="stSelectbox"] label {
            color: #66506f !important;
            font-weight: 800 !important;
            font-size: 1.02rem !important;
        }

        div[data-baseweb="select"] > div {
            border-radius: 16px !important;
            border-color: #e4d5eb !important;
            background-color: rgba(255, 255, 255, 0.95) !important;
        }

        .stButton > button {
            width: 100%;
            min-height: 3.15rem;
            border: 0;
            border-radius: 18px;
            color: white;
            font-size: 1.08rem;
            font-weight: 900;
            background: linear-gradient(90deg, #f49aba 0%, #b99be8 52%, #8ebde9 100%);
            box-shadow: 0 10px 24px rgba(179, 138, 206, 0.3);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 28px rgba(179, 138, 206, 0.38);
            color: white;
        }

        .result-heading {
            text-align: center;
            margin: 2rem 0 1rem 0;
            color: #5d466b;
            font-size: 1.75rem;
            font-weight: 900;
        }

        .fortune-card {
            height: 100%;
            min-height: 222px;
            padding: 1.25rem 1rem;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(231, 217, 239, 0.9);
            box-shadow: 0 12px 28px rgba(93, 70, 107, 0.09);
            text-align: center;
        }

        .fortune-icon {
            font-size: 2.3rem;
            line-height: 1;
        }

        .fortune-title {
            margin-top: 0.65rem;
            color: #5f4969;
            font-weight: 900;
            font-size: 1.15rem;
        }

        .stars {
            margin: 0.45rem 0 0.65rem 0;
            color: #f3a83b;
            font-size: 1.24rem;
            letter-spacing: 0.05rem;
            white-space: nowrap;
        }

        .fortune-text {
            color: #6f6075;
            line-height: 1.65;
            font-size: 0.96rem;
            word-break: keep-all;
        }

        .lucky-panel {
            margin-top: 1rem;
            padding: 1.15rem 1.2rem;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(255, 238, 246, 0.94), rgba(237, 244, 255, 0.94));
            border: 1px solid #eadfed;
            box-shadow: 0 12px 28px rgba(93, 70, 107, 0.08);
        }

        .lucky-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.7rem;
            margin-top: 0.7rem;
        }

        .lucky-item {
            padding: 0.85rem 0.55rem;
            border-radius: 18px;
            text-align: center;
            background: rgba(255, 255, 255, 0.72);
        }

        .lucky-label {
            color: #9a82a2;
            font-size: 0.84rem;
            font-weight: 700;
        }

        .lucky-value {
            margin-top: 0.18rem;
            color: #5f4969;
            font-size: 1.02rem;
            font-weight: 900;
        }

        .color-dot {
            display: inline-block;
            width: 0.82rem;
            height: 0.82rem;
            margin-right: 0.25rem;
            border-radius: 50%;
            vertical-align: -0.05rem;
            border: 1px solid rgba(0, 0, 0, 0.08);
        }

        .today-message {
            margin-top: 1rem;
            padding: 1rem 1.2rem;
            border-radius: 20px;
            text-align: center;
            background: rgba(255, 255, 255, 0.82);
            color: #66506f;
            font-weight: 800;
            line-height: 1.6;
        }

        .notice {
            margin-top: 1.5rem;
            text-align: center;
            color: #9a8a9f;
            font-size: 0.82rem;
        }

        @media (max-width: 640px) {
            .block-container {
                padding-top: 1.25rem;
            }

            .lucky-grid {
                grid-template-columns: 1fr;
            }

            .fortune-card {
                min-height: auto;
                margin-bottom: 0.5rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# 띠 및 운세 데이터
# ---------------------------------------------------------
ZODIACS = {
    "쥐띠": {"emoji": "🐭", "caption": "재치와 순발력이 반짝이는 하루"},
    "소띠": {"emoji": "🐮", "caption": "차분한 성실함이 행운을 부르는 하루"},
    "호랑이띠": {"emoji": "🐯", "caption": "용기 있는 선택이 빛나는 하루"},
    "토끼띠": {"emoji": "🐰", "caption": "다정한 마음이 좋은 인연을 만드는 하루"},
    "용띠": {"emoji": "🐲", "caption": "자신감 있는 도전이 돋보이는 하루"},
    "뱀띠": {"emoji": "🐍", "caption": "섬세한 판단력이 빛을 발하는 하루"},
    "말띠": {"emoji": "🐴", "caption": "활기찬 움직임이 기회를 만드는 하루"},
    "양띠": {"emoji": "🐑", "caption": "따뜻한 배려가 행복을 키우는 하루"},
    "원숭이띠": {"emoji": "🐵", "caption": "톡톡 튀는 아이디어가 반짝이는 하루"},
    "닭띠": {"emoji": "🐔", "caption": "꼼꼼한 준비가 결실로 이어지는 하루"},
    "개띠": {"emoji": "🐶", "caption": "진심 어린 태도가 신뢰를 얻는 하루"},
    "돼지띠": {"emoji": "🐷", "caption": "긍정적인 마음에 복이 찾아오는 하루"},
}

FORTUNE_TEXTS = {
    "재물운": {
        1: [
            "충동구매가 슬쩍 찾아올 수 있어요. 장바구니에 담아 두고 한 번 더 생각해 보세요.",
            "오늘은 크게 늘리기보다 지키는 날이에요. 작은 지출도 메모하면 도움이 돼요.",
            "예상하지 못한 지출이 생길 수 있어요. 꼭 필요한 것부터 차근차근 살펴보세요.",
        ],
        2: [
            "소소한 절약이 기분 좋은 결과로 이어져요. 작은 할인도 놓치지 마세요.",
            "돈을 쓰기 전에 우선순위를 정하면 만족도가 높아져요.",
            "나가는 돈을 가볍게 점검해 보세요. 생각보다 아낄 곳이 보일 수 있어요.",
        ],
        3: [
            "들어오고 나가는 흐름이 무난해요. 계획대로 움직이면 안정적인 하루예요.",
            "작은 행운이 찾아올 수 있어요. 다만 지나친 기대보다는 균형이 중요해요.",
            "필요한 곳에는 기분 좋게 쓰고, 불필요한 소비만 살짝 줄여 보세요.",
        ],
        4: [
            "알뜰한 선택이 빛나는 날이에요. 좋은 조건이나 반가운 혜택을 발견할 수 있어요.",
            "미뤄 둔 금전 계획을 정리하기 좋아요. 현실적인 아이디어가 떠오를 수 있어요.",
            "작은 이득이 모여 만족스러운 결과가 돼요. 꼼꼼하게 비교해 보세요.",
        ],
        5: [
            "재물운이 반짝반짝 빛나요! 좋은 기회가 보인다면 차분히 확인하고 잡아 보세요.",
            "뜻밖의 혜택이나 반가운 소식이 찾아올 수 있어요. 감사한 마음으로 누려 보세요.",
            "현명한 판단이 좋은 결과로 이어지는 날이에요. 자신 있게 계획을 실천해 보세요.",
        ],
    },
    "연애운": {
        1: [
            "말이 조금 다르게 전달될 수 있어요. 서두르지 말고 부드럽게 표현해 보세요.",
            "마음을 알아주길 기다리기보다 솔직한 한마디가 필요해요.",
            "작은 오해가 생길 수 있으니 상대의 이야기를 끝까지 들어 주세요.",
        ],
        2: [
            "먼저 따뜻하게 인사하면 어색한 분위기가 금방 풀릴 수 있어요.",
            "상대의 작은 장점을 찾아 칭찬해 보세요. 관계가 한층 부드러워져요.",
            "조금 천천히 다가가는 것이 좋아요. 편안한 대화부터 시작해 보세요.",
        ],
        3: [
            "편안하고 잔잔한 관계운이에요. 평소처럼 진심을 보여 주면 충분해요.",
            "친근한 대화 속에서 마음이 가까워질 수 있어요. 자연스러운 모습을 보여 주세요.",
            "가까운 사람에게 고마움을 표현하기 좋은 날이에요.",
        ],
        4: [
            "다정한 한마디가 좋은 분위기를 만들어요. 먼저 연락해도 좋은 날이에요.",
            "새로운 인연과 즐거운 대화가 시작될 수 있어요. 밝은 미소를 잊지 마세요.",
            "서로의 마음이 잘 통하는 날이에요. 함께하는 시간을 소중히 즐겨 보세요.",
        ],
        5: [
            "설렘 가득한 기운이 찾아왔어요! 진심을 표현하면 마음이 잘 전해질 수 있어요.",
            "매력이 반짝이는 날이에요. 있는 그대로의 자연스러운 모습이 가장 사랑스러워요.",
            "관계운이 활짝 피어나는 날이에요. 행복한 추억을 만들 기회를 놓치지 마세요.",
        ],
    },
    "학업운": {
        1: [
            "집중력이 잠시 흔들릴 수 있어요. 10분만 시작한다는 마음으로 책을 펼쳐 보세요.",
            "한꺼번에 많이 하려 하면 지칠 수 있어요. 가장 쉬운 것부터 하나씩 해결해 보세요.",
            "오늘은 속도보다 꾸준함이 중요해요. 짧게 공부하고 잠깐 쉬는 방법이 좋아요.",
        ],
        2: [
            "공부할 내용을 작게 나누면 부담이 줄어요. 체크리스트를 활용해 보세요.",
            "익숙한 내용부터 복습하면 집중력이 서서히 올라와요.",
            "혼자 막히는 부분은 질문해 보세요. 생각보다 쉽게 실마리를 찾을 수 있어요.",
        ],
        3: [
            "차분하게 계획을 따라가면 무난한 성과를 얻을 수 있어요.",
            "배운 내용을 짧게 정리하면 기억에 오래 남아요.",
            "오늘의 목표를 한 가지로 정하면 집중하기 쉬워요.",
        ],
        4: [
            "이해력과 집중력이 좋은 날이에요. 어려웠던 내용에 다시 도전해 보세요.",
            "새로운 내용을 배우기 좋아요. 핵심을 자신만의 말로 정리해 보세요.",
            "계획한 공부를 빠르게 끝낼 수 있어요. 남는 시간에는 복습까지 해보세요.",
        ],
        5: [
            "학업운이 최고예요! 집중이 잘되고 새로운 아이디어도 톡톡 떠오를 수 있어요.",
            "어려운 문제도 차근차근 풀면 답이 보여요. 자신감을 가지고 도전해 보세요.",
            "오늘 배운 내용이 쏙쏙 들어오는 날이에요. 중요한 과목을 먼저 공부해 보세요.",
        ],
    },
}

LUCKY_COLORS = [
    ("딸기우유 핑크", "#F7A8C4"),
    ("라벤더 보라", "#C8B6E8"),
    ("하늘빛 블루", "#9DCEF2"),
    ("민트 그린", "#A8E1D1"),
    ("레몬 크림", "#F7E59B"),
    ("복숭아 코랄", "#F4AD9D"),
    ("구름 화이트", "#F8F5F2"),
    ("포도 젤리", "#B99BD7"),
    ("살구 오렌지", "#F6BD8B"),
    ("새싹 그린", "#B8D99A"),
]

DAILY_MESSAGES = [
    "작은 용기가 오늘을 반짝이게 만들어요.",
    "완벽하지 않아도 괜찮아요. 한 걸음이면 충분해요.",
    "따뜻한 말 한마디가 행운을 데려올 거예요.",
    "오늘의 노력은 미래의 나에게 주는 선물이에요.",
    "나만의 속도로 가도 충분히 잘하고 있어요.",
    "웃을 일이 하나씩 늘어나는 하루가 될 거예요.",
    "좋은 기회는 준비된 마음에서 시작돼요.",
    "망설였던 일을 가볍게 시작해 보기 좋은 날이에요.",
    "소중한 사람에게 먼저 다정함을 건네 보세요.",
    "오늘의 작은 선택이 기분 좋은 변화를 만들어요.",
    "나는 생각보다 더 많은 가능성을 가지고 있어요.",
    "천천히 살펴보면 가까이에 행운이 보여요.",
]


# ---------------------------------------------------------
# 날짜와 띠를 이용한 고정 운세 생성 함수
# ---------------------------------------------------------
def fixed_index(key: str, length: int) -> int:
    """같은 문자열에는 언제나 같은 인덱스를 반환합니다."""
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % length


def make_fortune(zodiac: str) -> dict:
    date_key = today.isoformat()
    result = {
        "zodiac": zodiac,
        "date": date_key,
        "categories": {},
    }

    for category in ("재물운", "연애운", "학업운"):
        score_key = f"{date_key}|{zodiac}|{category}|score"
        score = fixed_index(score_key, 5) + 1

        texts = FORTUNE_TEXTS[category][score]
        text_key = f"{date_key}|{zodiac}|{category}|text"
        description = texts[fixed_index(text_key, len(texts))]

        result["categories"][category] = {
            "score": score,
            "description": description,
        }

    color_index = fixed_index(f"{date_key}|{zodiac}|color", len(LUCKY_COLORS))
    result["lucky_color"] = LUCKY_COLORS[color_index]
    result["lucky_number"] = fixed_index(f"{date_key}|{zodiac}|number", 99) + 1
    result["message"] = DAILY_MESSAGES[
        fixed_index(f"{date_key}|{zodiac}|message", len(DAILY_MESSAGES))
    ]

    return result


def star_text(score: int) -> str:
    return "★" * score + "☆" * (5 - score)


def fortune_card(icon: str, title: str, score: int, description: str) -> str:
    return f"""
        <div class="fortune-card">
            <div class="fortune-icon">{icon}</div>
            <div class="fortune-title">{title}</div>
            <div class="stars">{star_text(score)}</div>
            <div class="fortune-text">{description}</div>
        </div>
    """


# ---------------------------------------------------------
# 화면 구성
# ---------------------------------------------------------
st.markdown('<div class="main-title">🔮 몽글몽글 오늘의 띠 운세</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">나의 띠를 고르고 오늘 찾아온 행운을 확인해 보세요 ✨</div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="date-badge">📅 {today_text}</div>', unsafe_allow_html=True)

zodiac_names = list(ZODIACS.keys())
selected_zodiac = st.selectbox(
    "어떤 띠의 운세를 볼까요?",
    zodiac_names,
    format_func=lambda name: f"{ZODIACS[name]['emoji']}  {name}",
)

animal = ZODIACS[selected_zodiac]
st.markdown(
    f"""
    <div class="selection-box">
        <div class="animal-emoji">{animal["emoji"]}</div>
        <div class="animal-name">{selected_zodiac}</div>
        <div class="animal-caption">{animal["caption"]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 다른 띠를 고르면 이전 결과를 숨깁니다.
if st.session_state.get("selected_zodiac") != selected_zodiac:
    st.session_state["selected_zodiac"] = selected_zodiac
    st.session_state.pop("fortune_result", None)

if st.button("✨ 오늘의 운세 보기 ✨", type="primary"):
    st.session_state["fortune_result"] = make_fortune(selected_zodiac)
    st.balloons()

result = st.session_state.get("fortune_result")

if result and result["zodiac"] == selected_zodiac and result["date"] == today.isoformat():
    st.markdown(
        f'<div class="result-heading">{animal["emoji"]} {selected_zodiac}의 오늘 운세</div>',
        unsafe_allow_html=True,
    )

    icons = {"재물운": "💰", "연애운": "💗", "학업운": "📚"}
    columns = st.columns(3)

    for column, category in zip(columns, ("재물운", "연애운", "학업운")):
        data = result["categories"][category]
        with column:
            st.markdown(
                fortune_card(
                    icons[category],
                    category,
                    data["score"],
                    data["description"],
                ),
                unsafe_allow_html=True,
            )

    color_name, color_hex = result["lucky_color"]
    st.markdown(
        f"""
        <div class="lucky-panel">
            <div style="text-align:center; color:#5f4969; font-size:1.18rem; font-weight:900;">
                🍀 오늘의 행운 포인트
            </div>
            <div class="lucky-grid">
                <div class="lucky-item">
                    <div class="lucky-label">행운의 색</div>
                    <div class="lucky-value">
                        <span class="color-dot" style="background:{color_hex};"></span>
                        {color_name}
                    </div>
                </div>
                <div class="lucky-item">
                    <div class="lucky-label">행운의 숫자</div>
                    <div class="lucky-value">🎲 {result["lucky_number"]}</div>
                </div>
                <div class="lucky-item">
                    <div class="lucky-label">오늘의 띠</div>
                    <div class="lucky-value">{animal["emoji"]} {selected_zodiac}</div>
                </div>
            </div>
        </div>
        <div class="today-message">
            💌 오늘의 한마디<br>
            “{result["message"]}”
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="notice">
        ※ 이 운세는 재미로 즐기는 콘텐츠입니다. 중요한 결정은 충분히 고민한 뒤 내려 주세요.
    </div>
    """,
    unsafe_allow_html=True,
)
