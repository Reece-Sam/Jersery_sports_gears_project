import { createContext, useState } from "react";

import manUnited from "../assets/images/Man-united.jpg";
import realMadrid from "../assets/images/Real-Madrid-blue.jpg";
import realmadridAway from "../assets/images/Real-madrid-2021.jpg";

export const CartContext = createContext();

export function CartProvider({ children }) {
  const [cartItems, setCartItems] = useState([
    {
      id: 3,
      name: "Man United Home Jersey",
      image: manUnited,
      size: "XL",
      quantity: 1,
      price: 12000,
    },
  ]);

  const addToCart = (product) => {
    const existingItem = cartItems.find((item) => item.id === product.id);

    if (existingItem) {
      setCartItems(
        cartItems.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item,
        ),
      );
    } else {
      setCartItems([
        ...cartItems,
        {
          ...product,
          quantity: 1,
        },
      ]);
    }
  };

  return (
    <CartContext.Provider
      value={{
        cartItems,
        setCartItems,
        addToCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}
