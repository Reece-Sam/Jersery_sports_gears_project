import { useContext } from "react";
import { CartContext } from "../context/CartContext";
import CartItem from "../components/CartItem";
import "../css/cartPage.css";

function Cart() {
  const { cartItems, setCartItems } = useContext(CartContext);

  const increaseQuantity = (id) => {
    setCartItems(
      cartItems.map((item) =>
        item.id === id ? { ...item, quantity: item.quantity + 1 } : item,
      ),
    );
  };

  const decreaseQuantity = (id) => {
    setCartItems(
      cartItems.map((item) =>
        item.id === id && item.quantity > 1
          ? { ...item, quantity: item.quantity - 1 }
          : item,
      ),
    );
  };

  const removeItem = (id) => {
    setCartItems(cartItems.filter((item) => item.id !== id));
  };

  const shipping = 1000;

  const subtotal = cartItems.reduce(
    (total, item) => total + item.price * item.quantity,
    0,
  );

  const total = subtotal + shipping;

  return (
    <div className="cart-page">
      <div className="cart-container">
        <div className="cart-items">
          <h2>Shopping Cart</h2>

          {cartItems.length > 0 ? (
            cartItems.map((item) => (
              <CartItem
                key={item.id}
                item={item}
                increaseQuantity={() => increaseQuantity(item.id)}
                decreaseQuantity={() => decreaseQuantity(item.id)}
                removeItem={() => removeItem(item.id)}
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
