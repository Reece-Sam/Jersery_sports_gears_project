import {NavLink} from "react-router-dom";
import "../css/navbar.css";

function Navbar() {
    return (
      <nav className="navbar">
        <h2>THE LEAGUE</h2>

        <ul>
          <li>
            <NavLink to="/">Home</NavLink>
          </li>
          <li>
            <NavLink to="/cart">Cart</NavLink>
          </li>
          <li>
            <NavLink to="/orders">Orders</NavLink>
          </li>
          <li>
            <NavLink to="/login">Login</NavLink>
          </li>
        </ul>
      </nav>
    );
}      

export default Navbar;