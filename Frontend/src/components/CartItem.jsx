import "../css/cart.css";

function CartItem({ item }) {
    return (
        <div className="cart-item">
            <img src={item.image} alt={item.name} />

            <div className="cart-info">
                <h3>{item.name}</h3>
                <p>Size: {item.size}</p>
                <p>Quantity: {item.quantity}</p>
                <h4>{item.price}XAF</h4>

            </div>

        </div>
    );
}

export default CartItem;