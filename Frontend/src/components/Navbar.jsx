import {NavLink} from "react-router-dom";
import { useContext } from "react";
import { CartContext } from "../context/CartContext";
import "../css/navbar.css";

function Navbar() {
  const { cartItems } = useContext(CartContext);

  const cartCount = cartItems.reduce((total, item) => total + item.quantity, 0);

    return (
      <nav className="navbar">
        <h2>THE LEAGUE</h2>

        <ul>
          <li>
            <NavLink to="/">Home</NavLink>
          </li>
          <li>
            <NavLink to="/cart"> 🛒 Cart ({cartCount})</NavLink>
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