'use client';

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useEffect } from 'react';

// Fix for default marker icons in Next.js
// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface Violation {
    id: number;
    facility_name: string;
    violation_date: string;
    violation_type: string;
    location: string;
    summary: string;
    latitude: number;
    longitude: number;
}

interface MapProps {
    violations: Violation[];
}

const Map = ({ violations }: MapProps) => {
    // Center of India
    const position: [number, number] = [20.5937, 78.9629];

    return (
        <MapContainer center={position} zoom={5} style={{ height: '100%', width: '100%' }} className="z-0">
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {violations.map((v) => {
                // Use actual coordinates if available, otherwise default to center
                // Add slight jitter to prevent perfect stacking: (Math.random() - 0.5) * 0.05
                const lat = (v.latitude || 20.5937) + (Math.random() - 0.5) * 0.05;
                const lng = (v.longitude || 78.9629) + (Math.random() - 0.5) * 0.05;

                return (
                    <Marker key={v.id} position={[lat, lng]}>
                        <Popup>
                            <div className="p-2">
                                <h3 className="font-bold">{v.facility_name}</h3>
                                <p className="text-sm text-gray-600">{v.violation_date}</p>
                                <p className="text-sm font-semibold text-red-600">{v.violation_type}</p>
                                <p className="text-xs mt-2">{v.summary}</p>
                            </div>
                        </Popup>
                    </Marker>
                );
            })}
        </MapContainer>
    );
};

export default Map;
