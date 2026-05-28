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

  const handleSubmit = (e) => {
    e.preventDefault();

    if (
      !name ||
      !email ||
      !password ||
      !passwordCheck
    ) {
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

    alert("회원가입 완료!");

    navigate("/");
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
          </form>
        </div>
      </div>
    </div>
  );
}

export default SignupPage;