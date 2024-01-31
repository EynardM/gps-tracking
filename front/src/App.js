// Imports
import React, { useState } from 'react';
import WebSocketComponent from './components/WebSocketComponent';
import MapComponent from './components/MapComponent';

// App
const App = () => {
  // State variable to hold data received from WebSocket
  const [data, setData] = useState({});

  // Function to update data state with new data
  const handleDataUpdate = (newData) => {
    setData(newData);
  }

  return (
    <div>
      {/* WebSocket component to receive data updates */}
      <WebSocketComponent onDataUpdate={handleDataUpdate} />

      {/* Map component to display data */}
      <MapComponent data={data} />
    </div>
  );
};

export default App;
