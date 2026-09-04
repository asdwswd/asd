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
```python
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

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("영화 데이터를 다양한 그래프로 살펴봅니다.")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 숫자형 데이터 변환
    numeric_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 장르가 여러 개라면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("기타")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    df.loc[df["genre"] == "", "genre"] = "기타"

    # 영화명 결측치 처리
    df["movieNm"] = df["movieNm"].fillna("영화명 없음").astype(str)

    # 제작 국가 결측치 처리
    df["nation"] = df["nation"].fillna("기타").astype(str).str.strip()
    df.loc[df["nation"] == "", "nation"] = "기타"

    return df


try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.code(str(e))
    st.stop()


# --------------------------------------------------
# 1. 장르별 영화 편수 - 도넛 그래프
# --------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_count = df["genre"].value_counts().reset_index()
genre_count.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수",
)

fig_genre.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig_genre.update_layout(
    height=500,
    margin=dict(t=70, l=20, r=20, b=20)
)

st.plotly_chart(fig_genre, use_container_width=True)

st.markdown(
    """
    <div style="
        background-color: #f5f7fa;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 35px;
        border-left: 5px solid #555555;
    ">
        <b>📌 이 그래프로 알 수 있는 것</b><br>
        어떤 장르의 영화가 많이 만들어졌는지 한눈에 비교할 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 2. 장르 안의 영화 - 트리맵
# --------------------------------------------------
st.header("2. 장르별 영화와 총 관객수")

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].copy()

treemap_df = treemap_df.dropna(subset=["total_audi"])
treemap_df = treemap_df[treemap_df["total_audi"] >= 0]

fig_treemap = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화의 총 관객수",
)

fig_treemap.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig_treemap.update_layout(
    height=650,
    margin=dict(t=70, l=10, r=10, b=10)
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown(
    """
    <div style="
        background-color: #f5f7fa;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 35px;
        border-left: 5px solid #555555;
    ">
        <b>📌 이 그래프로 알 수 있는 것</b><br>
        각 장르 안에서 어떤 영화가 많은 관객을 모았는지 비교할 수 있습니다.
        칸이 클수록 총 관객수가 많습니다.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 3. 총 관객수 분포 - 히스토그램
# --------------------------------------------------
st.header("3. 총 관객수의 분포")

hist_df = df[
    ["movieNm", "total_audi"]
].copy()

hist_df = hist_df.dropna(subset=["total_audi"])
hist_df = hist_df[hist_df["total_audi"] >= 0]

fig_hist = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객수 분포",
    labels={
        "total_audi": "총 관객수",
        "count": "영화 수"
    }
)

fig_hist.update_traces(
    hovertemplate=(
        "관객수 구간: %{x}<br>"
        "영화 수: %{y}편"
        "<extra></extra>"
    )
)

fig_hist.update_layout(
    height=500,
    margin=dict(t=70, l=20, r=20, b=20)
)

st.plotly_chart(fig_hist, use_container_width=True)


# 가장 영화가 많이 몰린 구간 계산
if len(hist_df) > 0:

    min_audience = hist_df["total_audi"].min()
    max_audience = hist_df["total_audi"].max()

    if min_audience == max_audience:
        most_common_range = f"{min_audience:,.0f}명"
    else:
        bins = pd.cut(
            hist_df["total_audi"],
            bins=20,
            include_lowest=True
        )

        bin_counts = bins.value_counts().sort_index()

        most_common_bin = bin_counts.idxmax()

        lower_bound = most_common_bin.left
        upper_bound = most_common_bin.right

        most_common_range = (
            f"{lower_bound:,.0f}명 ~ {upper_bound:,.0f}명"
        )

    # 가장 관객이 많은 영화
    most_watched = hist_df.loc[
        hist_df["total_audi"].idxmax()
    ]

    max_movie_name = most_watched["movieNm"]
    max_audience = most_watched["total_audi"]

    st.markdown(
        f"""
        <div style="
            background-color: #f5f7fa;
            padding: 18px 22px;
            border-radius: 12px;
            margin-bottom: 35px;
            border-left: 5px solid #555555;
        ">
            <b>📌 이 그래프로 알 수 있는 것</b><br>
            대부분의 영화는 <b>{most_common_range}</b> 구간에 가장 많이 몰려 있습니다.<br>
            가장 많은 관객을 기록한 영화는
            <b>{max_movie_name}</b>으로,
            총 <b>{max_audience:,.0f}명</b>의 관객을 기록했습니다.
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# 4. 개봉일 스크린수와 총 관객수 - 산점도
# --------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객수의 관계")

scatter_df = df[
    ["movieNm", "genre", "first_scrn", "total_audi"]
].copy()

scatter_df = scatter_df.dropna(
    subset=["first_scrn", "total_audi"]
)

scatter_df = scatter_df[
    (scatter_df["first_scrn"] >= 0)
    & (scatter_df["total_audi"] >= 0)
]

fig_scatter = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객수",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre": "장르"
    }
)

fig_scatter.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객수: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig_scatter.update_layout(
    height=600,
    margin=dict(t=70, l=20, r=20, b=20)
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown(
    """
    <div style="
        background-color: #f5f7fa;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 35px;
        border-left: 5px solid #555555;
    ">
        <b>📌 이 그래프로 알 수 있는 것</b><br>
        개봉일에 스크린을 많이 확보한 영화가 실제로 더 많은 관객을 모았는지
        두 변수의 관계를 살펴볼 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 5. 영화가 10편 이상인 장르 - 상자 그림
# --------------------------------------------------
st.header("5. 장르별 총 관객수 상자 그림")

# 영화가 10편 이상인 장르만 선택
genre_movie_count = df["genre"].value_counts()

valid_genres = genre_movie_count[
    genre_movie_count >= 10
].index

box_df = df[
    df["genre"].isin(valid_genres)
][
    ["genre", "movieNm", "total_audi"]
].copy()

box_df = box_df.dropna(
    subset=["total_audi"]
)

box_df = box_df[
    box_df["total_audi"] >= 0
]

fig_box = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객수 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객수"
    }
)

fig_box.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{x}<br>"
        "총 관객수: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig_box.update_layout(
    height=600,
    showlegend=False,
    margin=dict(t=70, l=20, r=20, b=20)
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown(
    """
    <div style="
        background-color: #f5f7fa;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 35px;
        border-left: 5px solid #555555;
    ">
        <b>📌 이 그래프로 알 수 있는 것</b><br>
        영화가 10편 이상인 장르끼리 총 관객수의 중앙값과 분포를 비교할 수 있습니다.
        상자 밖에 표시되는 점은 해당 장르의 일반적인 범위에서 벗어난 영화이며,
        마우스를 올리면 영화명을 확인할 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 6. 개봉일 스크린수 × 총 관객수 × 첫 주 관객수
#    버블 산점도
# --------------------------------------------------
st.header("6. 첫 주 관객수를 크기로 표현한 버블 그래프")

bubble_df = df[
    [
        "movieNm",
        "genre",
        "first_scrn",
        "total_audi",
        "first_week_audi"
    ]
].copy()

bubble_df = bubble_df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi"
    ]
)

bubble_df = bubble_df[
    (bubble_df["first_scrn"] >= 0)
    & (bubble_df["total_audi"] >= 0)
    & (bubble_df["first_week_audi"] >= 0)
]

fig_bubble = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=45,
    title="개봉일 스크린수와 총 관객수 - 첫 주 관객수 버블",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "첫 주 관객수",
        "genre": "장르"
    }
)

fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{fullData.name}<br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객수: %{y:,.0f}명<br>"
        "첫 주 관객수: %{marker.size:,.0f}명"
        "<extra></extra>"
    )
)

fig_bubble.update_layout(
    height=650,
    margin=dict(t=70, l=20, r=20, b=20)
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown(
    """
    <div style="
        background-color: #f5f7fa;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 35px;
        border-left: 5px solid #555555;
    ">
        <b>📌 이 그래프로 알 수 있는 것</b><br>
        가로축은 개봉일 스크린수, 세로축은 총 관객수이며,
        버블이 클수록 첫 주에 많은 관객이 관람한 영화입니다.
        따라서 영화의 개봉 규모와 초반 흥행, 최종 흥행을 함께 비교할 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 7. 제작 국가 → 장르 - 선버스트
# --------------------------------------------------
st.header("7. 제작 국가에서 장르로 내려가는 선버스트")

sunburst_df = df[
    ["nation", "genre", "movieNm"]
].copy()

sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("기타")
    .astype(str)
    .str.strip()
)

sunburst_df["genre"] = (
    sunburst_df["genre"]
    .fillna("기타")
    .astype(str)
    .str.strip()
)

sunburst_df.loc[
    sunburst_df["nation"] == "",
    "nation"
] = "기타"

sunburst_df.loc[
    sunburst_df["genre"] == "",
    "genre"
] = "기타"


fig_sunburst = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    title="제작 국가 → 장르별 영화 편수",
)

fig_sunburst.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig_sunburst.update_layout(
    height=700,
    margin=dict(t=70, l=10, r=10, b=10)
)

st.plotly_chart(
    fig_sunburst,
    use_container_width=True
)

st.markdown(
    """
    <div style="
        background-color: #f5f7fa;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 35px;
        border-left: 5px solid #555555;
    ">
        <b>📌 이 그래프로 알 수 있는 것</b><br>
        제작 국가를 먼저 보고 그 안에서 어떤 장르의 영화가 많이 만들어졌는지
        단계적으로 확인할 수 있습니다. 영역이 클수록 해당 국가 또는 장르의
        영화 편수가 많다는 뜻입니다.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 끝
# --------------------------------------------------
st.divider()

st.caption("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
```

