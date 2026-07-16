import API_BASE_URL from "./api";

export async function getProducts() {
  const response = await fetch(`${API_BASE_URL}/api/products`);

  if (!response.ok) {
    throw new Error("Failed to fetch product");
  }

  return response.json();
}
