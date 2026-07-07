import CartItem from '../components/CartItem';
import manUnited from "../assets/images/Man-united.jpg";
import "../css/cartPage.css";

function Cart() {
    const item = {
      name: "Man United Home Jersey",
      image: manUnited,
      size: "XL",
      quantity: 1,
      price: 12000
    };

   const shipping = 1000;
   const subtotal = item.price * item.quantity;
   const total = subtotal + shipping;

   return (
    <div className="cart-page">
        <div className="cart-container">
            <div className="cart-items">
                <h2>Shopping Cart</h2>
                 
                <CartItem item={item} />
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

                <button className="checkout-btn">
                    Proceed to Checkout
                </button>

            </div>
        </div>
    </div>
   )
}

export default Cart;