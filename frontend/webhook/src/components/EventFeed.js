// src/EventFeed.js

import React, { useState, useEffect } from 'react';
import './EventFeed.css'; // We'll create this file for styling

// The URL of your Flask API backend
const API_URL = 'http://127.0.0.1:5000/events/latest?limit=20';

const EventFeed = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // useEffect hook to fetch data when the component mounts
    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await fetch(API_URL);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setEvents(data);
            } catch (e) {
                console.error("Failed to fetch events:", e);
                setError("Failed to load the event feed. Is the backend server running?");
            } finally {
                setLoading(false);
            }
        };

        fetchEvents();
        
        // Optional: Set up polling to refresh data every 30 seconds
        const intervalId = setInterval(fetchEvents, 30000);

        // Cleanup function to clear the interval when the component unmounts
        return () => clearInterval(intervalId);

    }, []); // The empty dependency array ensures this effect runs only once on mount

    // Helper function to render a single event
    const renderEvent = (event, index) => {
        let description = "An unknown event occurred.";

        switch (event.type) {
            case 'push':
                description = (
                    <span>
                        <strong>{event.author}</strong> pushed to branch <strong>{event.to_branch}</strong>
                    </span>
                );
                break;
            case 'pull_request':
                description = (
                    <span>
                        <strong>{event.author}</strong> opened a pull request from <strong>{event.from_branch}</strong> to <strong>{event.to_branch}</strong>
                    </span>
                );
                break;
            case 'merge':
                description = (
                    <span>
                        <strong>{event.author}</strong> merged branch <strong>{event.from_branch}</strong> into <strong>{event.to_branch}</strong>
                    </span>
                );
                break;
            default:
                break;
        }

        return (
            <div key={index} className="event-card">
                <div className={`icon icon-${event.type}`}></div>
                <div className="event-details">
                    <p>{description}</p>
                    <small className="timestamp">{event.timestamp}</small>
                </div>
            </div>
        );
    };

    if (loading) {
        return <div className="container"><h2>Loading Events...</h2></div>;
    }

    if (error) {
        return <div className="container error"><h2>Error</h2><p>{error}</p></div>;
    }

    return (
        <div className="container">
            <h1>GitHub Activity Feed</h1>
            <div className="event-list">
                {events.length > 0 ? events.map(renderEvent) : <p>No events to display.</p>}
            </div>
        </div>
    );
};

export default EventFeed;