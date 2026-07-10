import { useContext } from "react";
import { CartContext } from "../context/CartContext";
import ProductCard from "../components/ProductCard";
import "../css/home.css";

import realMadrid from "../assets/images/Real-Madrid-blue.jpg";
import chelsea from "../assets/images/Chelsea-2021.jpg";

const products = [
  {
    id: 1,
    name: "Real Madrid Blue Jersey",
    image: realMadrid,
    size: "XL",
    quantity: 1,
    price: 12000,
    
  },
  {
    id: 2,
    name: "Chelsea Jersey",
    image: chelsea,
    size: "XXL",
    quantity: 1,
    price: 11000,
  },
];

function Home() {
  const { addToCart } = useContext(CartContext);

  return (
    <div className="home">
      <h1>Latest Jerseys</h1>

      <div className="products-grid">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            addToCart={addToCart}
          />
        ))}
      </div>
    </div>
  );
}

export default Home;
