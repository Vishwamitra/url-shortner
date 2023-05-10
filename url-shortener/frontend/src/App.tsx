import Shortener from "./components/shortener";
import TopNav from "./components/TopNav";
import URL from "./components/url"
import './all.css'
function App() {
  return (
    <div>
      <TopNav />
      <Shortener />
      <URL />
    </div>
  );
}

export default App;
