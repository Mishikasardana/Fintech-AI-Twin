
import React from 'react';
import type { Receipt } from '../../types';
import Card from '../../components/common/Card';
import { ShoppingBagIcon, FilmIcon, GlobeAltIcon } from '../../components/icons/Icons';

const mockReceipts: Receipt[] = [
  { id: '1', vendor: 'SuperMart', amount: 125.67, date: '2023-10-26', category: 'Groceries', icon: ShoppingBagIcon },
  { id: '2', vendor: 'Cineplex', amount: 32.50, date: '2023-10-25', category: 'Entertainment', icon: FilmIcon },
  { id: '3', vendor: 'Global Airways', amount: 874.22, date: '2023-10-24', category: 'Travel', icon: GlobeAltIcon },
  { id: '4', vendor: 'The Corner Cafe', amount: 15.80, date: '2023-10-24', category: 'Dining', icon: ShoppingBagIcon },
  { id: '5', vendor: 'Shopify', amount: 29.99, date: '2023-10-23', category: 'Subscription', icon: ShoppingBagIcon },
  { id: '6', vendor: 'Gas Station', amount: 55.10, date: '2023-10-22', category: 'Transport', icon: ShoppingBagIcon },
];

const ReceiptItem: React.FC<{ receipt: Receipt }> = ({ receipt }) => {
  const Icon = receipt.icon;
  return (
    <div className="flex items-center space-x-4 p-4 bg-brand-primary rounded-lg hover:bg-gray-800 transition-colors cursor-pointer">
      <div className="p-3 bg-gray-700 rounded-full">
        <Icon className="w-6 h-6 text-brand-accent" />
      </div>
      <div className="flex-1">
        <p className="font-semibold text-brand-text-primary">{receipt.vendor}</p>
        <p className="text-sm text-brand-text-secondary">{receipt.category}</p>
      </div>
      <div className="text-right">
        <p className="font-bold text-lg text-brand-text-primary">${receipt.amount.toFixed(2)}</p>
        <p className="text-sm text-brand-text-secondary">{receipt.date}</p>
      </div>
    </div>
  );
};

const ReceiptList: React.FC = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold text-brand-text-primary mb-6">AI Receipt Feed</h1>
      <Card>
        <div className="space-y-4">
          {mockReceipts.map(receipt => (
            <ReceiptItem key={receipt.id} receipt={receipt} />
          ))}
        </div>
      </Card>
    </div>
  );
};

export default ReceiptList;
