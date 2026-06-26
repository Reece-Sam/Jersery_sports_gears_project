import {Link} from "react-router-dom";
import "../css/navbar.css";

function Navbar() {
    return (
      <nav className="navbar">
        <h2>THE LEAGUE</h2>

        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/cart">Cart</Link>
          </li>
          <li>
            <Link to="/orders">Orders</Link>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
        </ul>
      </nav>
    );
}      

export default Navbar;