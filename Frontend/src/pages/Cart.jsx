import { useState, useEffect } from "react";
import {
  getCart,
  removeCartItem,
  updateCartItem,
} from "../services/cartService";
import CartItem from "../components/CartItem";
import "../css/cartPage.css";

function Cart() {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const userId = localStorage.getItem("user_id");

  const loadCart = async () => {
    try {
      const data = await getCart(userId);
      setCartItems(data.items || []);
    } catch (error) {
      console.error("Error loading cart:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (userId) {
      loadCart();
    } else {
      setLoading(false);
    }
  }, []);

  // We'll connect these to the backend next
  const increaseQuantity = (id) => {
    setCartItems((prevItems) =>
      prevItems.map((item) =>
        item.cart_item_id === id
          ? { ...item, quantity: item.quantity + 1 }
          : item,
      ),
    );
  };

  const decreaseQuantity = (id) => {
    setCartItems((prevItems) =>
      prevItems.map((item) =>
        item.cart_item_id === id && item.quantity > 1
          ? { ...item, quantity: item.quantity - 1 }
          : item,
      ),
    );
  };

  const removeItem = (id) => {
    setCartItems((prevItems) =>
      prevItems.filter((item) => item.cart_item_id !== id),
    );
  };

  const shipping = 1000;

  const subtotal = cartItems.reduce(
    (total, item) => total + Number(item.price) * item.quantity,
    0,
  );

  const total = subtotal + shipping;

  if (loading) {
    return <h2>Loading cart...</h2>;
  }

  return (
    <div className="cart-page">
      <div className="cart-container">
        <div className="cart-items">
          <h2>Shopping Cart</h2>

          {cartItems.length > 0 ? (
            cartItems.map((item) => (
              <CartItem
                key={item.cart_item_id}
                item={item}
                increaseQuantity={() => increaseQuantity(item.cart_item_id)}
                decreaseQuantity={() => decreaseQuantity(item.cart_item_id)}
                removeItem={() => removeItem(item.cart_item_id)}
              />
            ))
          ) : (
            <p>Your cart is empty.</p>
          )}
        </div>

        <div className="order-summary">
          <h2>Order Summary</h2>

          <div className="summary-row">
            <span>Subtotal</span>
            <span>{subtotal.toLocaleString()} FCFA</span>
          </div>

          <div className="summary-row">
            <span>Shipping</span>
            <span>{shipping.toLocaleString()} FCFA</span>
          </div>

          <hr />

          <div className="summary-row total">
            <span>Total</span>
            <span>{total.toLocaleString()} FCFA</span>
          </div>

          <button className="checkout-btn">Proceed to Checkout</button>
        </div>
      </div>
    </div>
  );
}

export default Cart;
