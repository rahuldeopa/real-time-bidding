import React from 'react';

function AuctionList({ auctions }) {
  return (
    <div>
      <h2>Auction List</h2>
      <ul>
        {auctions.map((auction) => (
          <li key={auction.id}>{auction.item_name} - ${auction.starting_price}</li>
        ))}
      </ul>
    </div>
  );
}

export default AuctionList;
