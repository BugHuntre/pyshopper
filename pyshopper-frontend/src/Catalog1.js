import React from 'react';
import axios from 'axios';
import { Card, Button, Row, Col } from 'react-bootstrap';

const BASE_URL = 'http://127.0.0.1:5000';

function Catalog({ email, refreshCart, refreshWishlist, catalog }) {
  const addToCart = async (item) => {
    try {
      await axios.post(`${BASE_URL}/add-to-cart`, {
        email,
        item: { ...item, quantity: item.quantity || 1 }
      });
      refreshCart();
    } catch (err) {
      console.error(err?.response?.data || err.message);
      alert('Failed to add to cart');
    }
  };

  const addToWishlist = async (item) => {
    try {
      await axios.post(`${BASE_URL}/wishlist/add`, {
        email,
        item: { ...item, quantity: item.quantity || 1 }
      });
      refreshWishlist();
    } catch (err) {
      console.error(err?.response?.data || err.message);
      alert('Failed to add to wishlist');
    }
  };

  return (
    <div>
      <h4>🛍️ Catalog</h4>
      <Row>
        {catalog.map((item, idx) => (
          <Col md={4} className="mb-4" key={idx}>
            <Card className="h-100 shadow-sm">
              <Card.Body>
                <Card.Title>{item.name}</Card.Title>
                <Card.Text>₹{item.price} | Qty: 1</Card.Text>
                <div className="d-flex justify-content-between">
                  <Button variant="primary" size="sm" onClick={() => addToCart(item)}>
                    Add to Cart
                  </Button>
                  <Button variant="outline-secondary" size="sm" onClick={() => addToWishlist(item)}>
                    Wishlist
                  </Button>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}

export default Catalog;
