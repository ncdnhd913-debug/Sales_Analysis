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
        
        # 3. 요청하신 컬럼 자동 설정 로직
        # [품목명]이 있으면 기본값으로 선택, 없으면 첫 번째 컬럼 선택
        default_path = ['품목명'] if '품목명' in df.columns else [df.columns[0]]
        
        path_cols = st.sidebar.multiselect(
            "계층 구조를 선택하세요", 
            options=df.columns.tolist(),
            default=default_path
        )
        
        # [장부금액]이 있으면 기본값으로 선택
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        default_val_index = numeric_cols.index('장부금액') if '장부금액' in numeric_cols else 0
        
        value_col = st.sidebar.selectbox(
            "매출액(크기) 기준 컬럼", 
            options=numeric_cols,
            index=default_val_index
        )

        if path_cols and value_col:
            # 4. 트리맵 생성 (값이 0보다 큰 데이터만 표시하여 에러 방지)
            chart_data = df[df[value_col] > 0]
            
            fig = px.treemap(
                chart_data, 
                path=path_cols, 
                values=value_col,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                # 이미지와 유사한 느낌을 위해 폰트 크기 및 색상 조정 가능
            )

            fig.update_traces(
                textinfo="label+value+percent entry",
                hovertemplate='<b>%{label}</b><br>매출액: %{value:,.0f}원<br>비중: %{percentEntry:.2%}'
            )
            
            fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))

            # 5. 화면 출력
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("분석할 품목명과 매출액 컬럼을 선택해 주세요.")

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에서 매출 데이터를 업로드해 주세요.")
