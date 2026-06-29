import "../css/productCard.css";

function ProductCard({ product }) {
  return (
    <div className="product-card">
      <img src={product.image_url} alt={product.name} />

      <h3>{product.name}</h3>

      <p>{product.price} XAF</p>

      <button>Add To Cart</button>
    </div>
  );
}

export default ProductCard;




// import "../css/productCard.css";
// import chelseaImage from "../assets/images/Something-chels.png";

// function ProductCard() {
//   return (
//     <div className="product-card">
//       <img src= {chelseaImage}  alt= "somethings chels"  />

//       <h3>Chelsea Jersey</h3>

//       <p>12000 XAF</p>

//       <button>Add To Cart</button>
//     </div>
//   );
// }

// export default ProductCard;
