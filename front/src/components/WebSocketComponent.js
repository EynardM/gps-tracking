// Imports
import { useEffect } from 'react';
import config from './Config';

// Component
const WebSocketComponent = ({ onDataUpdate }) => {
  useEffect(() => {
    // Establish WebSocket connection with api
    const socket = new WebSocket("ws://"+config.ipAddress+":15010/ws");

    // Listener for incoming messages
    socket.onmessage = (event) => {
      
      // Parse incoming data (twice cause otherwise we got string 😒 )
      const dataJSON = JSON.parse(JSON.parse(event.data)); 
     
      // Showing what we receive here
      console.info("Received in websocket component : ",dataJSON);
      
      // Update parent component with incoming data
      onDataUpdate(dataJSON);
    };  
  }, [onDataUpdate]);
};

// Export
export default WebSocketComponent;
