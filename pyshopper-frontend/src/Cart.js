import React from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Button, ListGroup, Alert } from 'react-bootstrap';

const BASE_URL = 'http://127.0.0.1:5000';

function Cart({ email, cart, refreshCart }) {
  const navigate = useNavigate();

  const removeFromCart = async (itemName) => {
    try {
      await axios.post(`${BASE_URL}/cart/remove-item`, {
        email,
        item_name: itemName,
      });
      refreshCart();
    } catch {
      alert('❌ Failed to remove item');
    }
  };

  const totalCost = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleProceedToCheckout = () => {
    navigate('/checkout');
  };

  return (
    <Card>
      <Card.Header>🛒 Your Cart</Card.Header>
      <Card.Body>
        {cart.length > 0 ? (
          <>
            <ListGroup variant="flush">
              {cart.map((item, idx) => (
                <ListGroup.Item key={idx} className="d-flex justify-content-between align-items-center">
                  <div>
                    {item.name} — ₹{item.price} × {item.quantity}
                  </div>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => removeFromCart(item.name)}
                  >
                    Remove
                  </Button>
                </ListGroup.Item>
              ))}
            </ListGroup>

            <h5 className="mt-4">🧾 Total: ₹{totalCost.toFixed(2)}</h5>
            <Button className="mt-3" variant="success" onClick={handleProceedToCheckout}>
              ✅ Proceed to Checkout
            </Button>
          </>
        ) : (
          <Alert variant="secondary" className="mb-0">Your cart is empty.</Alert>
        )}
      </Card.Body>
    </Card>
  );
}

export default Cart;
