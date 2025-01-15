import React, { useState } from 'react';

function BidForm() {
  const [bidAmount, setBidAmount] = useState('');
  const [message, setMessage] = useState('');

  const handleBidSubmit = async () => {
    if (!bidAmount) {
      setMessage("Please enter a bid amount.");
      return;
    }

    try {
      const response = await fetch("http://backend:8000/place_bid/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            auction_id: 1,
            user_id: 2,
            amount: 1000
        })
    });
    

      if (response.ok) {
        const data = await response.json();
        setMessage(data.status);  // Display success message
      } else {
        const errorData = await response.json();
        setMessage(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error placing bid:", error);
      setMessage("Failed to place bid. Please try again.");
    }
  };

  return (
    <div>
      <h2>Place a Bid</h2>
      <input
        type="number"
        value={bidAmount}
        onChange={(e) => setBidAmount(e.target.value)}
        placeholder="Enter bid amount"
      />
      <button onClick={handleBidSubmit}>Place Bid</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default BidForm;
