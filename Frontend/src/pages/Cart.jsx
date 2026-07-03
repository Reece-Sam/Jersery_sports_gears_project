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

    return (
        <div className="cart-page">
            <h2>Shopping Cart</h2>

            <CartItem item={item} />
        </div>
    );
}

export default Cart;