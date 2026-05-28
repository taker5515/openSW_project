import { Link } from "react-router-dom";
import Header from "../Components/Header";
import "../PageStyles/MainPage.css";

function MainPage() {
  return (
    <div>
      <Header />

      <main className="main">
        <section className="hero">
          <p className="sub">주식 뉴스 이메일 서비스</p>

          <h1>
            관심 있는 주식 뉴스를 <br />
            이메일로 받아보세요
          </h1>

          <p className="desc">
            AI, 반도체, 전기차 등 다양한 테마의 뉴스를
            쉽고 빠르게 확인할 수 있습니다.
          </p>

      
        </section>

        <section className="cards">
          <Link to="/theme" className="card">
            <h3>전체 뉴스</h3>
            <p>최신 뉴스를 한눈에</p>
          </Link>

          <div className="card">
            <h3>이메일 구독</h3>
            <p>뉴스를 메일로 받아보기</p>
          </div>

          <Link to="/dashboard?tab=overview" className="card">
            <h3>빠른 정보</h3>
            <p>시장 흐름을 빠르게 파악</p>
          </Link>
        </section>
      </main>
    </div>
  );
}

export default MainPage;