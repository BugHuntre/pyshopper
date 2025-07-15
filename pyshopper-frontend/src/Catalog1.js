import React from 'react';
import { Card, Button, Row, Col } from 'react-bootstrap';
import { addItemToCart, addItemToWishlist } from './api';


function Catalog({ email, refreshCart, refreshWishlist, catalog }) {
 const addToCart = async (item) => {
  try {
    await addItemToCart(email, item);
    refreshCart();
  } catch (err) {
    console.error(err?.response?.data || err.message);
    alert('Failed to add to cart');
  }
};


  const addToWishlist = async (item) => {
  try {
    await addItemToWishlist(email, item);
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
