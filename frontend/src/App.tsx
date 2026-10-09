import React from 'react';
import { RouterProvider } from 'react-router-dom';
import { router } from './routes';
import { Providers } from './app/providers';

function App() {
  return (
    <Providers>
      <RouterProvider router={router} />
    </Providers>
  );
}

export default App;
