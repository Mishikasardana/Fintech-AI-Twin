
import React from 'react';
import Card from '../../components/common/Card';
import { SparklesIcon } from '../../components/icons/Icons';

interface PlaceholderScreenProps {
  title: string;
  message: string;
}

const PlaceholderScreen: React.FC<PlaceholderScreenProps> = ({ title, message }) => {
  return (
    <div>
      <h1 className="text-3xl font-bold text-brand-text-primary mb-6">{title}</h1>
      <Card className="text-center">
        <div className="py-16">
          <SparklesIcon className="w-16 h-16 mx-auto text-brand-accent mb-4" />
          <h2 className="text-2xl font-semibold text-brand-text-primary mb-2">Feature Coming Soon</h2>
          <p className="text-brand-text-secondary max-w-md mx-auto">{message}</p>
        </div>
      </Card>
    </div>
  );
};

export default PlaceholderScreen;
