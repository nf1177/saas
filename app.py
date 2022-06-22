import pandas as pd
import streamlit as st
import time
import altair as alt

# データの読みこみ
pd.options.display.precision = 2
data = pd.read_csv("saas.csv")

# data = data.round({'リスク値': 0})
# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="SaaS：検索",
                   page_icon=":computer:")

# 画像読み込み

# Use local CSS


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- スライドバー ----
st.sidebar.write("""## 以下の情報を入力してください""")
category_1 = st.sidebar.selectbox(
    'カテゴリーを選択してください。：', data["カテゴリ1"].unique())
data = data[data["カテゴリ1"] == category_1]

category_2 = st.sidebar.selectbox(
    'カテゴリーを選択してください。：', data["カテゴリ2"].unique())


# ---- 節水効果 ----
df_selection = data.query(
    "カテゴリ1 == @category_1 & カテゴリ2 ==@category_2")


st.header("SaaSのリスク値と使用値")


with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("SaaS一覧")
        st.dataframe(df_selection, width=1500, height=800)

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("SaaSのリスク値と使用率")
        points = alt.Chart(df_selection).mark_point(size=200).encode(
            x=alt.X('リスク値', scale=alt.Scale(domain=[5, 100])),
            y='使用率',
            tooltip=['サービス名称', "リスク値", "使用率"]
        )

        text = points.mark_text(
            align='left',
            baseline='middle',
            dx=10,
            dy=10
        ).encode(
            text='サービス名称'
        )

        st.altair_chart((points+text).interactive(), use_container_width=True)
