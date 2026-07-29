const API_URL = "http://127.0.0.1:5000/api/cart";

export async function addToCart(userId, productId, quantity = 1, size) {
  const response = await fetch("http://127.0.0.1:5000/api/cart/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: userId,
      product_id: productId,
      quantity,
      size,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message);
  }

  return data;
}

export async function getCart(userId) {
  const response = await fetch(`${API_URL}/${userId}`);

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message);
  }

  return data;
}

export async function removeCartItem(itemId) {
  const response = await fetch(`${API_URL}/item/${itemId}`, {
    method: "DELETE",
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message);
  }

  return data;
}

export async function updateCartItem(itemId, quantity) {
  const response = await fetch(`${API_URL}/item/${itemId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      quantity,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message);
  }

  return data;
}