import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Header from "../Components/Header";
import "../PageStyles/LoginPage.css";

const THEME_OPTIONS = [
  { label: "기술/미디어", value: "tech&media" },
  { label: "소비/생활", value: "consumer&life" },
  { label: "산업/에너지/부동산", value: "industry&energy&realEstate" },
  { label: "금융", value: "finance" },
  { label: "헬스케어/공공", value: "HC&pub" },
];

function LoginPage() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [selectedThemes, setSelectedThemes] = useState([]);

  const handleSubmit = async () => {
    if (!email || !password) {
      alert("이메일과 비밀번호를 입력해주세요.");
      return;
    }
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user_email", email);
        navigate("/");
      } else {
        const err = await res.json();
        alert(err.detail || "로그인에 실패했습니다.");
      }
    } catch {
      alert("서버 연결에 실패했습니다.");
    }
  };

  const toggleTheme = (value) => {
    setSelectedThemes((prev) =>
      prev.includes(value) ? prev.filter((t) => t !== value) : [...prev, value]
    );
  };

  const handleSaveThemes = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("로그인 후 테마를 저장할 수 있습니다.");
      return;
    }
    try {
      const res = await fetch("/api/users/me/themes", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ themes: selectedThemes }),
      });
      if (res.ok) {
        alert("테마가 저장됐습니다.");
      } else {
        alert("테마 저장에 실패했습니다.");
      }
    } catch {
      alert("서버 연결에 실패했습니다.");
    }
  };

  return (
    <div>
      <Header />

      <main className="login-page">
        <section className="login-container">
          <div className="login-box">
            <div className="input-group">
              <label>email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>password</label>

              <div className="password-wrapper">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
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

            <button className="login-submit" onClick={handleSubmit}>
              로그인
            </button>

            <Link to="/signup" className="signup-link">
              회원가입
            </Link>
          </div>

          <div className="theme-box">
            {THEME_OPTIONS.map(({ label, value }) => (
              <label key={value} className="theme-item">
                <input
                  type="checkbox"
                  checked={selectedThemes.includes(value)}
                  onChange={() => toggleTheme(value)}
                />
                <span>{label}</span>
              </label>
            ))}

            <button className="theme-save-btn" onClick={handleSaveThemes}>
              정보를 받을 테마 저장
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default LoginPage;
