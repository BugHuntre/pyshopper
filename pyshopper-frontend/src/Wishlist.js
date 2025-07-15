import React from 'react';
import axios from 'axios';
import { Card, Button, ListGroup, Alert, ButtonGroup } from 'react-bootstrap';

const BASE_URL = 'http://127.0.0.1:5000';

function Wishlist({ email, wishlist, refreshCart, refreshWishlist }) {
  const moveToCart = async (item_name) => {
    try {
      await axios.post(`${BASE_URL}/wishlist/move-to-cart`, {
        email,
        item_name,
      });
      refreshCart();
      refreshWishlist();
    } catch {
      alert('❌ Failed to move item to cart');
    }
  };

  const removeFromWishlist = async (item_name) => {
    try {
      await axios.post(`${BASE_URL}/wishlist/remove`, {
        email,
        item_name,
      });
      refreshWishlist();
    } catch {
      alert('❌ Failed to remove item from wishlist');
    }
  };

  return (
    <div>
      <h4>💖 Wishlist</h4>
      {wishlist.length > 0 ? (
        <Card className="mb-3 shadow-sm">
          <ListGroup variant="flush">
            {wishlist.map((item, idx) => (
              <ListGroup.Item
                key={idx}
                className="d-flex justify-content-between align-items-center"
              >
                <div>
                  {item.name} — ₹{item.price} × {item.quantity}
                </div>
                <ButtonGroup>
                  <Button
                    variant="success"
                    size="sm"
                    onClick={() => moveToCart(item.name)}
                  >
                    Move to Cart
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => removeFromWishlist(item.name)}
                  >
                    Remove
                  </Button>
                </ButtonGroup>
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Card>
      ) : (
        <Alert variant="secondary">Your wishlist is empty.</Alert>
      )}
    </div>
  );
}

export default Wishlist;
