import Header from "./components/Header.jsx";
import Hero from "./components/Hero.jsx";
import About from "./components/About.jsx";
import DemoVideo from "./components/DemoVideo.jsx";
import Team from "./components/Team.jsx";
import Contact from "./components/Contact.jsx";
import Footer from "./components/Footer.jsx";
import DiagnosticResult from "./components/DiagnosticResult.jsx";
import InputPage from "./components/InputPage.jsx";

export default function App() {
  const path = window.location.pathname;
  if (path === "/diagnosis-result" || path === "/diagnosis-result/") return <DiagnosticResult />;
  if (path === "/new-diagnosis" || path === "/new-diagnosis/") return <InputPage />;
  return <><Header /><main><Hero /><About /><DemoVideo /><Team /><Contact /></main><Footer /></>;
}
