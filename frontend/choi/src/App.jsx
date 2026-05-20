import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./Pages/MainPage";
import LoginPage from "./Pages/LoginPage";
import ThemePage from "./Pages/ThemePage";
import Dashboard from "./Pages/Dashboard/App";
import NewsPage from "./Pages/NewsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/theme" element={<ThemePage />} />
        <Route path="/theme/:themeName" element={<ThemePage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/news/:newsId" element={<NewsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;