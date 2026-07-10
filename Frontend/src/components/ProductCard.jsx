import "../css/productCard.css";

function ProductCard({ product, addToCart }) {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />

      <h3>{product.name}</h3>

      <p>{product.price.toLocaleString()} FCFA</p>

      <button onClick={() => addToCart(product)}>Add To Cart</button>
    </div>
  );
}

export default ProductCard;
