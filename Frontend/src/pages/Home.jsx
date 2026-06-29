import ProductCard from "../components/ProductCard";
import "../css/home.css";

import realMadrid from "../assets/images/Real-Madrid-blue.jpg";
import chelsea from "../assets/images/Chelsea-2021.jpg";

  const products = [
    {
      id: 1,
      name: "Real Madrid blue Jersey",
      price: 12000,
      image_url: realMadrid,
    },
    {
      id: 2,
      name: "Chelsea Jersey",
      price: 11000,
      image_url: chelsea,
    },
  ];

function Home() {
  return (
    <div className="home">
      <h1>Latest Jerseys</h1>
      <div className="products-grid">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}

export default Home;
