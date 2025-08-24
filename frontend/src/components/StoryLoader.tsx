import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from "react-router-dom";
import axios from 'axios';
import LoadingStatus from "./LoadingStatus";
import StoryGame from "./StoryGame";
import { API_BASE_URL } from "../util";
import type {Story} from '../types/story';

const StoryLoader: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [story, setStory] = useState<Story | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (id) {
            void loadStory(id);
        }
    }, [id]);

    const loadStory = async (storyId: string) => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.get<Story>(`${API_BASE_URL}/stories/${storyId}/complete`);
            setStory(response.data);
            setLoading(false);
        } catch (err: any) {
            if (err.response?.status === 404) {
                setError("Story is not found.");
            } else {
                setError("Failed to load story");
            }
        } finally {
            setLoading(false);
        }
    };

    const createNewStory = () => {
        navigate("/");
    };

    if (loading) {
        return <LoadingStatus theme={"story"} />;
    }

    if (error) {
        return (
            <div className="story-loader">
                <div className="error-message">
                    <h2>Story Not Found</h2>
                    <p>{error}</p>
                    <button onClick={createNewStory}>Go to Story Generator</button>
                </div>
            </div>
        );
    }

    if (story) {
        return (
            <div className="story-loader">
                <StoryGame story={story} onNewStory={createNewStory} />
            </div>
        );
    }

    return null;
};

export default StoryLoader;