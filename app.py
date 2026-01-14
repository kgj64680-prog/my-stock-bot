import streamlit as st
import yfinance as yf
from openai import OpenAI
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="김건진의 AI 주식 비서", layout="wide")
st.title("🏛️ AI 주식 분석 및 시장 수급 리포트")

# 2. 보안 키 설정 (나중에 Streamlit 설정에서 숨길 수 있습니다)
with st.sidebar:
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
    client = OpenAI(api_key=api_key) if api_key else None
    st.info("이 웹사이트는 김건진님의 PC를 끄셔도 작동합니다.")

# 3. 기능 선택 (탭 메뉴)
tab1, tab2 = st.tabs(["📊 종목 심층 분석", "🔥 오늘의 주도 테마"])

# --- [기능 1: 종목 분석] ---
with tab1:
    symbol = st.text_input("분석할 종목 코드를 입력하세요 (예: NVDA, 005930.KS)").upper()
    if st.button("분석 시작") and client:
        with st.spinner("AI가 리포트를 작성 중입니다..."):
            stock = yf.Ticker(symbol)
            info = stock.fast_info
            prompt = f"Analyze {symbol} (Current Price: {info.last_price}). Provide a professional investment report in Korean."
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            st.markdown(res.choices[0].message.content)

# --- [기능 2: 오늘의 테마] ---
with tab2:
    if st.button("오늘의 수급 테마 확인하기") and client:
        with st.spinner("시장 데이터를 읽어오는 중..."):
            # 주요 종목들로 시장 상황 파악
            tickers = ["005930.KS", "000660.KS", "005380.KS", "035420.KS", "373220.KS"]
            market_data = ""
            for t in tickers:
                s = yf.Ticker(t)
                change = ((s.fast_info.last_price - s.fast_info.open) / s.fast_info.open) * 100
                market_data += f"{t}: {change:.2f}% / "
            
            prompt = f"Based on: {market_data}, explain today's Korean stock market themes in Korean with a table."
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            st.success("오늘의 시장 분석 완료!")
            st.markdown(res.choices[0].message.content)