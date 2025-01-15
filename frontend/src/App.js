import React, { useState, useEffect } from 'react';
import AuctionList from './components/AuctionList';
import BidForm from './components/BidForm';
import Notifications from './components/Notifications';

function App() {
  const [auctions, setAuctions] = useState([]);
  const [notification, setNotification] = useState('');

  useEffect(() => {
    // Fetch auction data from backend (or use mock data)
    fetch('http://localhost:8000/auctions')
      .then((response) => response.json())
      .then((data) => setAuctions(data));

    const socket = new WebSocket('ws://localhost:8000/ws/bid_updates');
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotification(`New bid placed: $${data.amount} by User ${data.user_id}`);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div className="App">
      <h1>Real-Time Bidding</h1>
      <AuctionList auctions={auctions} />
      <BidForm />
      <Notifications message={notification} />
    </div>
  );
}

export default App;
