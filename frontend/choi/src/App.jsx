import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./Pages/MainPage";
import LoginPage from "./Pages/LoginPage";
import ThemePage from "./Pages/ThemePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/theme/:themeName" element={<ThemePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;