import React from 'react';
import { Card, Button, ListGroup, Alert, ButtonGroup } from 'react-bootstrap';
import {
  moveWishlistItemToCart,
  removeItemFromWishlist
} from './api';

function Wishlist({ email, wishlist, refreshCart, refreshWishlist }) {
  const moveToCart = async (itemName) => {
    try {
      await moveWishlistItemToCart(email, itemName);
      refreshCart();
      refreshWishlist();
    } catch {
      alert('❌ Failed to move item to cart');
    }
  };

  const removeFromWishlist = async (itemName) => {
    try {
      await removeItemFromWishlist(email, itemName);
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
