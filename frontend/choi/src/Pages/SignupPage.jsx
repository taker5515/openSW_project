import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "../firebase"; 
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../PageStyles/SignupPage.css";

function SignupPage() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordCheck, setPasswordCheck] = useState("");
  const [agree, setAgree] = useState(false);

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;
      const res = await fetch("/api/auth/google", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: user.email, name: user.displayName }),
      });
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user_email", user.email);
      }
      alert(`${user.displayName}님 환영합니다!`);
      navigate("/");
    } catch (error) {
      console.log("구글 로그인 에러 코드:", error.code);
      if (
        error.code === "auth/popup-closed-by-user" ||
        error.code === "auth/cancelled-popup-request"
      ) {
        return;
      }
      alert(`구글 로그인 실패: ${error.code}`);
    }
  };
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!name || !email || !password || !passwordCheck) {
      alert("모든 항목을 입력해주세요.");
      return;
    }
    if (password !== passwordCheck) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }
    if (!agree) {
      alert("정보수신 동의가 필요합니다.");
      return;
    }

    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });
      if (res.ok) {
        alert("회원가입이 완료됐습니다. 로그인해주세요.");
        navigate("/login");
      } else {
        const err = await res.json();
        alert(err.detail || "회원가입에 실패했습니다.");
      }
    } catch {
      alert("서버 연결에 실패했습니다.");
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-container">
        <div className="signup-box">
          <h1>회원가입</h1>

          <form onSubmit={handleSubmit}>
            <div className="signup-input-group">
              <label>이름</label>
              <input
                type="text"
                placeholder="이름을 입력하세요"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="signup-input-group">
              <label>이메일</label>
              <input
                type="email"
                placeholder="이메일을 입력하세요"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="signup-input-group">
              <label>비밀번호</label>
              <input
                type="password"
                placeholder="비밀번호를 입력하세요"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <div className="signup-input-group">
              <label>비밀번호 확인</label>
              <input
                type="password"
                placeholder="비밀번호를 다시 입력하세요"
                value={passwordCheck}
                onChange={(e) => setPasswordCheck(e.target.value)}
              />
            </div>

            <div className="agree-box">
              <input
                type="checkbox"
                id="agree"
                checked={agree}
                onChange={(e) => setAgree(e.target.checked)}
              />

              <label htmlFor="agree">
                정보수신 및 이용약관에 동의합니다.
              </label>
            </div>

            <button className="signup-submit" type="submit">
              회원가입
            </button>
            <button
            type="button"
            className="google-signup-btn"
            onClick={handleGoogleLogin}
            >
                Google로 회원가입
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default SignupPage;