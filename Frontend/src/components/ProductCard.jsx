import "../css/productCard.css";

function ProductCard() {
  return (
    <div className="product-card">
      <img src= "src/assets/images/Something-chels.png"  alt= "somethings chels"  />

      <h3>Chelsea Jersey</h3>

      <p>12000 XAF</p>

      <button>Add To Cart</button>
    </div>
  );
}

export default ProductCard;
