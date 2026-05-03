import os
import json
import yfinance as yf
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

# 1. 환경 변수 및 AI 설정
load_dotenv()
# .env 파일에 GEMINI_API_KEY="본인키" 가 있어야 합니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

# 2. 데이터 요청 형식 정의
class StockRequest(BaseModel):
    ticker: str

# 3. 주식 분석 API 엔드포인트
@app.post("/analyze")
async def analyze_stock(request: StockRequest):
    try:
        # yfinance로 최신 뉴스 가져오기
        stock = yf.Ticker(request.ticker)
        news_list = stock.news[:3] # 최신 뉴스 3개만 추출
        
        if not news_list:
            raise HTTPException(status_code=404, detail="관련 뉴스를 찾을 수 없습니다.")

        results = []
        for news in news_list:
            # AI에게 뉴스 분석 요청
            prompt = f"""
            주식 종목 '{request.ticker}'에 대한 다음 뉴스를 분석해주세요.
            제목: {news['title']}
            
            반드시 아래 JSON 형식으로만 한국어로 응답하세요:
            {{
                "summary": "뉴스 내용을 3줄로 핵심 요약",
                "sentiment": "호재 / 악재 / 중립 중 선택",
                "reason": "그렇게 판단한 이유를 짧게 설명"
            }}
            """
            response = model.generate_content(prompt)
            
            # JSON 데이터 파싱
            try:
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                analysis = json.loads(clean_text)
            except:
                # AI 응답이 JSON 형식이 아닐 경우를 대비한 예외 처리
                analysis = {"summary": "요약 실패", "sentiment": "알 수 없음", "reason": "AI 응답 파싱 오류"}

            results.append({
                "title": news['title'],
                "summary": analysis['summary'],
                "sentiment": analysis['sentiment'],
                "reason": analysis['reason'],
                "url": news['link']
            })
            
        return results # 최종 데이터를 JSON 리스트로 반환

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. 서버 실행 설정
if __name__ == "__main__":
    # 포트는 팀원들과 상의 후 결정 (기본 8000 사용)
    uvicorn.run(app, host="0.0.0.0", port=8000)