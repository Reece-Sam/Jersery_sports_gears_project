import { useState } from "react";
import "../css/productCard.css";
import { addToCart } from "../services/cartService";

function ProductCard({ product }) {
  const [size, setSize] = useState("M");

  const handleAddToCart = async () => {
    const userId = localStorage.getItem("user_id");

    if (!userId) {
      alert("Please login first.");
      return;
    }

    try {
      await addToCart(userId, product.id, 1, size);
      alert("Product added to cart!");
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="product-card">
      <img src={product.image_url} alt={product.name} />

      <h3>{product.name}</h3>

      <p>{product.price.toLocaleString()} FCFA</p>

      <div className="size-container">
        <label>Size</label>

        <select value={size} onChange={(e) => setSize(e.target.value)}>
          <option value="S">S</option>
          <option value="M">M</option>
          <option value="L">L</option>
          <option value="XL">XL</option>
          <option value="XXL">XXL</option>
        </select>
      </div>

      <button onClick={handleAddToCart}>Add To Cart</button>
    </div>
  );
}

export default ProductCard;
