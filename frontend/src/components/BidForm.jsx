import React, { useState } from 'react';

function BidForm() {
  const [bidAmount, setBidAmount] = useState('');
  
  const handleBidSubmit = async () => {
    // API call to place a bid (POST request)
    const response = await fetch('http://localhost:8000/place_bid/', {
      method: 'POST',
      body: JSON.stringify({
        auction_id: 1,  // Example auction ID
        user_id: 1,     // Example user ID
        amount: bidAmount
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    console.log(data);
  };

  return (
    <div>
      <h2>Place Bid</h2>
      <input 
        type="number" 
        value={bidAmount} 
        onChange={(e) => setBidAmount(e.target.value)} 
        placeholder="Enter bid amount" 
      />
      <button onClick={handleBidSubmit}>Place Bid</button>
    </div>
  );
}

export default BidForm;
