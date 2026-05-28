import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./Pages/MainPage";
import LoginPage from "./Pages/LoginPage";
import ThemePage from "./Pages/ThemePage";
import NewsPage from "./Pages/NewsPage";
import SignupPage from "./Pages/SignupPage"; 

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/theme/:themeName" element={<ThemePage />} />
        <Route path="/news/:id" element={<NewsPage />} />
        <Route path="/signup" element={<SignupPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;