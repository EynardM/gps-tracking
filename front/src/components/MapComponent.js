// Imports
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import '../App.css';
import Snowfall from 'react-snowfall';

// Icons
var Icon = L.Icon.extend({
  options: {
    iconSize:     [64, 64],
    popupAnchor:  [0, -20]
  }
});

var blackIcon = new Icon({
  iconUrl: "https://img.icons8.com/cotton/64/christmas-penguin.png",
});

var purpleIcon = new Icon({
  iconUrl: "https://img.icons8.com/arcade/64/christmas-penguin.png",
});

var grayIcon = new Icon({
  iconUrl: "https://img.icons8.com/dusk/64/christmas-penguin.png",
});

var blueIcon = new Icon({
  iconUrl: "https://img.icons8.com/keek/100/experimental-christmas-penguin-keek.png",
});

// Component
const MapComponent = ({ data }) => {
  // State variables
  const [markerPositions, setMarkerPositions] = useState({});
  const [pathLines, setPathLines] = useState({});
  const icons = [blackIcon, blueIcon, grayIcon, purpleIcon];
  const center = [-73.49491815199443,169.6962659072567];

  // Positions of penguins received
  useEffect(() => {
    if (data && data.ip && data.lat && data.lon) {
      setMarkerPositions(prevPositions => ({
        ...prevPositions,
        [data.ip]: [...(prevPositions[data.ip] || []), [data.lat, data.lon]]
      }));
    }
  }, [data]);

  // Lines between positions for each penguin
  useEffect(() => {
    const colors = ["black", "blue", "gray", "purple"];
    const newLines = {};
    Object.entries(markerPositions).forEach(([ip, positions], index) => {
      newLines[ip] = <Polyline key={ip} positions={positions} color={colors[index]} />;
    });
    setPathLines(newLines);
  }, [markerPositions]);

  return (
    <div className="background">
      <h2 style={{ textAlign: "center", fontFamily: "Soin Sans Pro, sans-serif", fontSize: "30px", fontWeight: "bold", color: "#084B8A"}}>Penguin GPS Tracker</h2>
      <Snowfall color="white" className="snowfall"/>
      <MapContainer center={center} zoom={10} className="map-container">
        <TileLayer 
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" 
          className="glacial-tile-layer" 
        />
        {Object.entries(markerPositions).map(([ip, position], index) => (
          <Marker key={ip} position={position[position.length - 1]} icon={icons[index % icons.length]}>
            <Popup>
              IP: {ip} <br/>
              Coordinates: (lat: {position[position.length - 1][0]}, lon: {position[position.length - 1][1]})
            </Popup>
          </Marker>
        ))}
        {Object.values(pathLines)}
      </MapContainer>
    </div>
  );
};

// Export
export default MapComponent;
