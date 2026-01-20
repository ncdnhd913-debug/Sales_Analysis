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
    # 데이터 불러오기
    try:
        df = pd.read_excel(uploaded_file)
        
        # 데이터 확인용 (상위 5개)
        with st.expander("업로드 데이터 확인"):
            st.write(df.head())

        # 사용자로부터 컬럼 선택 받기 (자동 추정 또는 수동 선택)
        st.sidebar.markdown("---")
        st.sidebar.subheader("컬럼 설정")
        
        # 카테고리(계층) 설정 - 예: ['대분류', '중분류', '상품명']
        path_cols = st.sidebar.multiselect(
            "계층 구조를 순서대로 선택하세요", 
            options=df.columns.tolist(),
            default=[df.columns[0]] # 기본값으로 첫 번째 컬럼
        )
        
        # 수치 데이터 선택 - 예: '매출액'
        value_col = st.sidebar.selectbox(
            "매출액(크기) 기준 컬럼을 선택하세요", 
            options=df.select_dtypes(include=['number']).columns.tolist()
        )

        if path_cols and value_col:
            # 3. Plotly 트리맵 생성
            # 색상은 우선 단일 색상 계열로 설정 (요청하신 대로 크기 위주)
            fig = px.treemap(
                df, 
                path=path_cols, 
                values=value_col,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            # 텍스트 정보 및 레이아웃 수정
            fig.update_traces(textinfo="label+value+percent entry")
            fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))

            # 4. 화면 출력
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("분석할 컬럼들을 선택해 주세요.")

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에서 매출 데이터를 업로드해 주세요.")
    # 샘플 가이드 이미지 등을 보여줄 수 있습니다.
