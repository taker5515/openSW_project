import { Link } from "react-router-dom";
import Header from "../components/Header";
import "../styles/MainPage.css";

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

          <div className="buttons">
            <button className="primary">뉴스 보러가기</button>
            <Link to="/login" className="secondary">구독 시작</Link>
          </div>
        </section>

        <section className="cards">
          <div className="card">
            <h3>테마별 뉴스</h3>
            <p>원하는 테마 뉴스만 모아서 제공</p>
          </div>

          <div className="card">
            <h3>이메일 구독</h3>
            <p>뉴스를 메일로 받아보기</p>
          </div>

          <div className="card">
            <h3>빠른 정보</h3>
            <p>시장 흐름을 빠르게 파악</p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default MainPage;
