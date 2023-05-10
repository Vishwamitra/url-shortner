function TopNav() {
  const headerList = ["Merge", "Quick", "Insert", "Heap", "Bubble"];
  return (
    <div className="h-100 d-flex align-items-center justify-content-center">
  
  <nav className="navbar navbar-expand-lg navbar-light bg-light">
  <a className="navbar-brand" href="#">
        <img src="/images/logo.png" width="30" height="30" alt="" />
        
      </a>

      <div className="collapse navbar-collapse" id="navbarNav">
    <ul className="navbar-nav">
      <li className="nav-item active">
        <a className="nav-link" href="#">Welcome to URL Shortener - Group 12<span className="sr-only">(current)</span></a>
          </li>
        </ul>
        </div>
  
      </nav>
      </div>
  );
}

export default TopNav;
