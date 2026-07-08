import "../css/cart.css";

function CartItem({ 
    item, 
    increaseQuantity, 
    decreaseQuantity,
    removeItem, 
}) {
    return (
        <div className="cart-item">
            <img src={item.image} alt={item.name} />

            <div className="cart-info">
                <h3>{item.name}</h3>
                <p>Size: {item.size}</p>
                <div className="quantity-controls">
                    <button onClick={decreaseQuantity}>-</button>

                    <span>{item.quantity}</span>

                    <button onClick={increaseQuantity}>+</button>
                </div>

                <button className="remove-btn" onClick={removeItem}>
                    Remove
                </button>
                <h4>{item.price.toLocaleString()} FCFA</h4>

            </div>

        </div>
    );
}

export default CartItem;