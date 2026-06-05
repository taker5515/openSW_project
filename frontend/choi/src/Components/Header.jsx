import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../PageStyles/Header.css";

function Header() {
  const [userEmail, setUserEmail] = useState(() => localStorage.getItem("user_email"));
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_email");
    setUserEmail(null);
    navigate("/");
  };

  return (
    <header className="header">
      <div className="header-inner">
        <Link to="/" className="logo">
          Stock Newsletter
        </Link>

        <nav className="nav">
          <Link to="/theme/tech&media">기술/미디어</Link>
          <Link to="/theme/consumer&life">소비/생활</Link>
          <Link to="/theme/industry&energy&realEstate">산업/에너지/부동산</Link>
          <Link to="/theme/finance">금융</Link>
          <Link to="/theme/HC&pub">헬스케어/공공</Link>
        </nav>

        {userEmail ? (
          <button className="login-btn" onClick={handleLogout}>
            로그아웃
          </button>
        ) : (
          <Link to="/login" className="login-btn">
            로그인
          </Link>
        )}
      </div>
    </header>
  );
}

export default Header;
