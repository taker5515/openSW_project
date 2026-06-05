// ==========================
// 0. API 기본 주소
// ==========================
const API_BASE_URL = window.API_BASE_URL || "http://localhost:8000";

// ==========================
// 1. 주식 차트 (TradingView)
// ==========================
function loadChart() {
  const script = document.createElement("script");
  script.src = "https://s3.tradingview.com/tv.js";
  script.onload = () => {
    new TradingView.widget({
      container_id: "chart",
      width: "100%",
      height: 400,
      symbol: "NASDAQ:AAPL", // 애플 (나중에 바꿔도 됨)
      interval: "D",
      theme: "light",
      style: "1",
      locale: "kr"
    });
  };
  document.body.appendChild(script);
}

loadChart();


// ==========================
// 2. 뉴스 불러오기
// ==========================
document.getElementById("loadNews").addEventListener("click", async () => {
  const list = document.getElementById("newsList");
  list.innerHTML = "<li>불러오는 중...</li>";
  try {
    const res = await fetch(`${API_BASE_URL}/api/news`);
    if (!res.ok) throw new Error(`서버 응답 오류: ${res.status}`);
    const data = await res.json();

    list.innerHTML = "";
    const items = Array.isArray(data) ? data : (data.items || []);
    if (items.length === 0) {
      list.innerHTML = "<li>뉴스가 없습니다.</li>";
      return;
    }
    items.forEach(news => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="${news.url}" target="_blank">${news.title}</a>`;
      list.appendChild(li);
    });

  } catch (err) {
    console.error("뉴스 로드 실패:", err);
    list.innerHTML = `<li style="color:red">뉴스를 불러오지 못했습니다. 백엔드 서버(${API_BASE_URL})가 실행 중인지 확인하세요.</li>`;
  }
});


// ==========================
// 3. AI 요약
// ==========================
document.getElementById("summaryBtn").addEventListener("click", async () => {
  const summaryEl = document.getElementById("summary");
  summaryEl.textContent = "요약 생성 중...";
  try {
    const res = await fetch(`${API_BASE_URL}/api/ai/summary`);
    if (!res.ok) throw new Error(`서버 응답 오류: ${res.status}`);
    const data = await res.json();
    summaryEl.textContent = data.summary || "요약 결과가 없습니다.";
  } catch (err) {
    console.error("요약 실패:", err);
    summaryEl.textContent = `요약을 불러오지 못했습니다. 백엔드 서버(${API_BASE_URL})가 실행 중인지 확인하세요.`;
  }
});