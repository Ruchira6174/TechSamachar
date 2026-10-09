import React from 'react';

export const LoadingState = () => (
  <div className="flex justify-center items-center h-48">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
  </div>
);

export const ErrorState = ({ message = "Something went wrong. Please try again." }: { message?: string }) => (
  <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-700 my-4">
    <p>{message}</p>
  </div>
);

export const EmptyState = ({ message = "No items found." }: { message?: string }) => (
  <div className="flex flex-col items-center justify-center p-8 text-center bg-gray-50 border border-dashed border-gray-300 rounded-lg my-4">
    <p className="text-gray-500">{message}</p>
  </div>
);
