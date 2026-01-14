import streamlit as st
import yfinance as yf
from openai import OpenAI
import pandas as pd
import time

# 1. 페이지 설정
st.set_page_config(page_title="김건진의 AI 주식 비서", layout="wide")
st.title("🏛️ AI 주식 분석 및 시장 수급 리포트")

# 2. 보안 키 설정
with st.sidebar:
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
    client = OpenAI(api_key=api_key) if api_key else None
    st.info("야후 파이낸스 차단 에러를 방지하기 위해 '안전 모드'로 작동 중입니다.")

# 3. 기능 탭
tab1, tab2 = st.tabs(["📊 종목 심층 분석", "🔥 오늘의 주도 테마"])

# --- [기능 1: 종목 분석] ---
with tab1:
    symbol = st.text_input("분석할 종목 코드를 입력하세요 (예: NVDA, 005930.KS)").upper()
    if st.button("분석 시작") and client:
        with st.spinner("AI가 데이터를 수집하고 분석 중입니다..."):
            try:
                # 차단 방지를 위해 주가를 가져오는 방식을 더 단순화함
                stock = yf.Ticker(symbol)
                # 에러가 자주 나는 fast_info 대신 history 사용
                hist = stock.history(period="1d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    price_info = f"현재가: {current_price:.2f}"
                else:
                    price_info = "가격 정보를 가져오지 못했으나 분석을 진행합니다."

                prompt = f"Analyze the stock {symbol}. {price_info}. Provide a professional investment report in Korean including target price and risks."
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                st.markdown(res.choices[0].message.content)
            except Exception as e:
                st.error(f"데이터 수집 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요. (에러: {e})")

# --- [기능 2: 오늘의 테마] ---
with tab2:
    if st.button("오늘의 수급 테마 확인하기") and client:
        with st.spinner("시장 상황 분석 중..."):
            # 차단 방지를 위해 리스트를 줄이고 요청 간격을 둠
            tickers = ["005930.KS", "000660.KS", "035420.KS", "373220.KS"]
            market_data = ""
            
            for t in tickers:
                try:
                    s = yf.Ticker(t)
                    h = s.history(period="2d")
                    if len(h) >= 2:
                        change = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                        market_data += f"{t}: {change:.2f}% / "
                    time.sleep(0.5) # 요청 간격 조절 (차단 방지)
                except:
                    continue
            
            prompt = f"Based on: {market_data}, explain today's Korean stock market themes in Korean with a table."
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            st.success("시장 분석 완료!")
            st.markdown(res.choices[0].message.content)
