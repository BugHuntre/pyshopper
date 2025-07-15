import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Spinner, Alert, Button, Card } from 'react-bootstrap';
import { checkoutCart, getReceiptDownloadUrl } from './api';


function Checkout() {
  const [receipt, setReceipt] = useState('');
  const [fileName, setFileName] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const email = localStorage.getItem('email');

  useEffect(() => {
  const doCheckout = async () => {
  try {
    const res = await checkoutCart(email);
    setReceipt(res.data.receipt_preview);
    setFileName(res.data.receipt_file);
    setLoading(false);
  } catch (err) {
    alert(err?.response?.data?.error || '❌ Checkout failed');
    navigate('/dashboard');
  }
};

    doCheckout();
  }, [email, navigate]);

const handleDownload = () => {
  const url = getReceiptDownloadUrl(fileName);
  window.open(url, '_blank');
};


  return (
    <Container className="py-4">
      <h3 className="mb-4">✅ Order Confirmed</h3>

      {loading ? (
        <div className="text-center mt-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-3">Generating your receipt...</p>
        </div>
      ) : (
        <>
          <Card className="mb-4">
            <Card.Header>📄 Receipt Preview</Card.Header>
            <Card.Body>
              <pre className="bg-light p-3 border rounded" style={{ whiteSpace: 'pre-wrap' }}>
                {receipt}
              </pre>
            </Card.Body>
          </Card>

          <div className="d-flex gap-3">
            <Button variant="outline-primary" onClick={handleDownload}>
              📥 Download Receipt
            </Button>

            <Button variant="secondary" onClick={() => navigate('/dashboard')}>
              🔙 Back to Dashboard
            </Button>
          </div>
        </>
      )}
    </Container>
  );
}

export default Checkout;
