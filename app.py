import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="매출 분석 히트맵")

# 2. 사이드바: 파일 업로드
st.sidebar.header("데이터 업로드")
uploaded_file = st.sidebar.file_uploader("ERP 매출 엑셀 파일을 선택하세요", type=["xlsx", "xls"])

st.title("📊 매출 비중 분석 히트맵")

if uploaded_file is not None:
    try:
        # 데이터 불러오기
        df = pd.read_excel(uploaded_file)
        
        with st.expander("업로드 데이터 확인"):
            st.write(df.head())

        st.sidebar.markdown("---")
        st.sidebar.subheader("컬럼 설정")
        
        # [품목명] 자동 선택
        default_path = ['품목명'] if '품목명' in df.columns else [df.columns[0]]
        path_cols = st.sidebar.multiselect(
            "계층 구조를 선택하세요", 
            options=df.columns.tolist(),
            default=default_path
        )
        
        # [장부금액] 자동 선택
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        default_val_index = numeric_cols.index('장부금액') if '장부금액' in numeric_cols else 0
        value_col = st.sidebar.selectbox(
            "매출액(크기) 기준 컬럼", 
            options=numeric_cols,
            index=default_val_index
        )

        if path_cols and value_col:
            # ---------------------------------------------------------
            # 중요: 오류 해결을 위한 데이터 전처리 (Aggregation)
            # ---------------------------------------------------------
            # 1. 선택된 컬럼들에서 결측치(NaN) 제거
            clean_df = df.dropna(subset=path_cols + [value_col])
            
            # 2. 계층 구조가 꼬이지 않도록 데이터 그룹화 (중복 품목 합치기)
            # 이 과정이 없으면 'is not a leaf' 오류가 발생할 수 있습니다.
            chart_data = clean_df.groupby(path_cols, as_index=False)[value_col].sum()
            
            # 3. 매출액이 0보다 큰 데이터만 필터링
            chart_data = chart_data[chart_data[value_col] > 0]
            # ---------------------------------------------------------

            # 트리맵 생성
            fig = px.treemap(
                chart_data, 
                path=path_cols, 
                values=value_col,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            fig.update_traces(
                textinfo="label+value+percent entry",
                hovertemplate='<b>%{label}</b><br>매출액: %{value:,.0f}원<br>비중: %{percentEntry:.2%}'
            )
            
            fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))

            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("분석할 품목명과 매출액 컬럼을 선택해 주세요.")

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에서 매출 데이터를 업로드해 주세요.")
