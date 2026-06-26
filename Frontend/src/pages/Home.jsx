import ProductCard from "../components/ProductCard";
import "../css/home.css";

function Home() {
  const products = [
    {
      id: 1,
      name: "Real Madrid blue Jersey",
      price: 12000,
      image_url:
        "src/assets/images/pexels-franklin-nwokoma-2155224311-33726647.jpg",
    },
    {
      id: 2,
      name: "Chelsea Jersey",
      price: 11000,
      image_url: "src/assets/images/simon-reza-YofQmnc-wns-unsplash.jpg",
    },
  ];

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
