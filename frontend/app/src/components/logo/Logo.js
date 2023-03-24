import logo from "./logo.png";
import './Logo.css'

function Logo() {
  return (
    <div className="Logo">
      <header className="Logo-header">
        <img src={logo} className="Logo-image" alt="logo" stile={{ width: "10%"}}/>
      </header>
    </div>
  );
}


export default Logo