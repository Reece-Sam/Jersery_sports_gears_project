import { useState } from 'react';
import CartItem from '../components/CartItem';
import manUnited from "../assets/images/Man-united.jpg";
import "../css/cartPage.css";

function Cart() {
    const [quantity, setQuantity] = useState(1);

    const increaseQuantity = () => {
        setQuantity(quantity + 1);
    };

    const decreaseQuantity = () => {
        if (quantity > 1) {
          setQuantity(quantity - 1);
        }
    };

    const removeItem = (id) => {
        setCartItems(cartItems.filter((item) => item.id !== id));
    }


    const [cartItems, setCartItems] = useState([
     {    
      id: 1,  
      name: "Man United Home Jersey",
      image: manUnited,
      size: "XL",
      quantity: quantity,
      price: 12000,
     },
    ]);

   const shipping = 1000;
   const subtotal = cartItems.reduce(
      (total, item) => total + item.price * item.quantity, 0
   )
   const total = subtotal + shipping;

   return (
    <div className="cart-page">
        <div className="cart-container">
            <div className="cart-items">
                <h2>Shopping Cart</h2>
            {cartItems.map((item) => (     
                <CartItem 
                  key={item.id}
                  item={item} 
                  increaseQuantity={increaseQuantity}
                  decreaseQuantity={decreaseQuantity}
                  removeItem={() => removeItem(item.id)}
                />
            ))}

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