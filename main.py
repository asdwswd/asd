import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    "1년간 박스오피스 10위권에 든 영화 가운데 해당 기간에 개봉한 "
    "216편의 데이터를 살펴봅니다."
)

st.divider()

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르가 여러 개일 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("기타")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 빈 장르는 기타로 처리
    df.loc[df["genre"] == "", "genre"] = "기타"

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.code(str(e))
    st.stop()


# --------------------------------------------------
# 데이터 확인
# --------------------------------------------------
st.caption(f"총 {len(df):,}편의 영화 데이터를 불러왔습니다.")

# --------------------------------------------------
# 그래프 1. 장르별 영화 편수
# --------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

genre_count["label"] = (
    genre_count["genre"]
    + " ("
    + genre_count["count"].astype(str)
    + "편)"
)

fig_genre = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수"
)

fig_genre.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig_genre.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=70, b=20),
    legend_title_text="장르",
    showlegend=True
)

st.plotly_chart(
    fig_genre,
    use_container_width=True
)

# --------------------------------------------------
# 그래프로 알 수 있는 것
# --------------------------------------------------
st.markdown(
    """
    <div style="
        background-color: #f5f7fa;
        padding: 18px 22px;
        border-radius: 12px;
        margin-top: 5px;
        margin-bottom: 30px;
        border-left: 5px solid #555555;
    ">
        <b>📌 이 그래프로 알 수 있는 것</b><br>
        장르별로 영화가 몇 편씩 분포되어 있는지 한눈에 비교할 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 향후 그래프를 추가할 수 있는 구역
# --------------------------------------------------
st.header("2. 다른 그래프")

st.info(
    "이 아래 구역에 영화 데이터의 다른 분포와 관계를 보여 주는 "
    "그래프를 추가할 수 있습니다."
)
