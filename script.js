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
  try {
    // 👉 나중에 백엔드 주소로 바꿔
    const res = await fetch("http://localhost:5000/api/news");
    const data = await res.json();

    const list = document.getElementById("newsList");
    list.innerHTML = "";

    data.forEach(news => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="${news.url}" target="_blank">${news.title}</a>`;
      list.appendChild(li);
    });

  } catch (err) {
    console.error(err);
    alert("뉴스 불러오기 실패");
  }
});


// ==========================
// 3. AI 요약
// ==========================
document.getElementById("summaryBtn").addEventListener("click", async () => {
  try {
    const res = await fetch("http://localhost:5000/api/summary");
    const data = await res.json();

    document.getElementById("summary").innerText = data.summary;

  } catch (err) {
    console.error(err);
    alert("요약 실패");
  }
});