import { Link } from "react-router-dom";
import "../PageStyles/Header.css";

function Header() {
  return (
    <header className="header">
      <div className="header-inner">
        <Link to="/" className="logo">
          Stock Newsletter
        </Link>

        <nav className="nav">
          <Link to="/theme/AI">AI</Link>
          <Link to="/theme/semiconductor">반도체</Link>
          <Link to="/theme/ev">전기차</Link>
          <Link to="/theme/bio">바이오</Link>
          <Link to="/theme/finance">금융</Link>
        </nav>

        <Link to="/login" className="login-btn">
          로그인
        </Link>
      </div>
    </header>
  );
}

export default Header;