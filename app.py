import streamlit as st
import yfinance as yf
from openai import OpenAI
import time

# 1. 페이지 설정
st.set_page_config(page_title="김건진의 AI 주식 비서", layout="wide")
st.title("🏛️ AI 주식 분석 및 시장 수급 리포트")

# 2. Secrets에서 API 키 가져오기
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("Secrets에 API Key를 설정해주세요.")
    st.stop()

# 3. 기능 탭
tab1, tab2 = st.tabs(["📊 종목 심층 분석", "🔥 오늘의 주도 테마"])

with tab1:
    symbol = st.text_input("분석할 종목 코드를 입력하세요 (예: NVDA, 005930.KS)").upper()
    if st.button("분석 시작"):
        with st.spinner("AI 분석 중..."):
            try:
                # 에러 방지를 위해 간단히 종목만 확인
                stock = yf.Ticker(symbol)
                prompt = f"Identify {symbol} and provide a professional investment report in Korean including target price and risks."
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                st.markdown(res.choices[0].message.content)
            except Exception as e:
                st.error(f"오류 발생: {e}")

with tab2:
    if st.button("오늘의 수급 테마 확인하기"):
        with st.spinner("시장 상황 분석 중..."):
            tickers = ["005930.KS", "000660.KS", "035420.KS", "373220.KS"]
            prompt = f"Explain today's Korean stock market themes focusing on these tickers: {', '.join(tickers)}. Write in Korean with a table."
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            st.success("시장 분석 완료!")
            st.markdown(res.choices[0].message.content)
import streamlit as st
# ... 기존 라이브러리들 ...

# 1. 접속 비밀번호 설정 (사이드바)
with st.sidebar:
    user_password = st.text_input("접속 암호를 입력하세요", type="password")

# 2. 비밀번호가 맞을 때만 실행되도록 제한
if user_password == "rlarjswls5%": # 김건진님만 아는 암호를 정하세요!
    # --- 여기서부터 기존 분석 코드 ---
    st.title("🏛️ 김건진의 AI 주식 비서")
    # ... (기존 코드 생략) ...
else:
    st.warning("암호를 입력해야 분석 기능을 사용할 수 있습니다.")
    st.stop() # 암호가 틀리면 여기서 멈춤
