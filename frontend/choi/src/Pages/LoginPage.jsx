import { useState } from "react";
import { Link } from "react-router-dom";

import Header from "../Components/Header";
import "../PageStyles/LoginPage.css";

function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div>
      <Header />

      <main className="login-page">
        <section className="login-container">
          <div className="login-box">
            <div className="input-group">
              <label>email</label>
              <input type="email" />
            </div>

            <div className="input-group">
              <label>password</label>

              <div className="password-wrapper">
                <input
                  type={showPassword ? "text" : "password"}
                />

                <button
                  type="button"
                  className="show-password-btn"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? "숨기기" : "보기"}
                </button>
              </div>
            </div>

            <button className="login-submit">
              로그인
            </button>

            <Link to="/signup" className="signup-link">
              회원가입
            </Link>
          </div>

          <div className="theme-box">
            <label className="theme-item">
              <input type="checkbox" />
              <span>기술/미디어</span>
            </label>

            <label className="theme-item">
              <input type="checkbox" />
              <span>소비/생활</span>
            </label>

            <label className="theme-item">
              <input type="checkbox" />
              <span>산업/에너지/부동산</span>
            </label>

            <label className="theme-item">
              <input type="checkbox" />
              <span>금융</span>
            </label>

            <label className="theme-item">
              <input type="checkbox" />
              <span>헬스케어/공공</span>
            </label>

            <button className="theme-save-btn">
              정보를 받을 테마 저장
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default LoginPage;
