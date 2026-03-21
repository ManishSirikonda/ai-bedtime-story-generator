import { useState, useEffect, useRef } from "react";
import StoryInput from "./components/StoryInput";
import ContinueForm from "./components/ContinueForm";
import { generateStory, continueStory } from "./api";
import "./App.css";

export default function App() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  
  // We now store an ARRAY of story parts to keep track of continuity!
  const [storyParts, setStoryParts] = useState<string[]>([]);
  
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const storiesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the bottom when a new story part is added
  useEffect(() => {
    storiesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [storyParts]);

  const handleGenerate = async (theme: string) => {
    setLoading(true); 
    setError("");
    try {
      const data = await generateStory(theme);
      if (data.status === "rejected") { 
        setError(data.reason); 
      } else {
        setSessionId(data.session_id);
        // Start a fresh story
        setStoryParts([data.story]);
      }
    } catch (e) {
      setError("Failed to connect to the backend. Is it running?");
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = async (feedback: string) => {
    if (!sessionId) return;
    setLoading(true); 
    setError("");
    try {
      const data = await continueStory(sessionId, feedback);
      if (data.status === "rejected") { 
        setError(data.reason); 
      } else {
        // APPEND the new chapter to our existing story array
        setStoryParts(prev => [...prev, data.story]);
      }
    } catch (e) {
      setError("Failed to connect to the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-wrapper">
      <div className="blobs">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
      </div>
      
      <div className="app">
        <header className="app-header">
          <div className="header-badge">AI Powered</div>
          <h1>Bedtime Storyteller</h1>
          <p>A magical, guided journey into the unknown.</p>
        </header>
        
        <main className="app-main">
          {storyParts.length === 0 && (
            <div className="glass-panel init-panel">
              <StoryInput onSubmit={handleGenerate} loading={loading} />
              {error && <div className="error-card" style={{marginTop: '1.5rem'}}>⚠️ {error}</div>}
            </div>
          )}
          
          {storyParts.length > 0 && (
            <div className="story-journey">
              {storyParts.map((part, index) => (
                <div key={index} className="glass-panel story-card fade-in">
                  <div className="chapter-marker">Chapter {index + 1}</div>
                  {/* format paragraphs */}
                  {part.split("\n").filter(p => p.trim() !== "").map((text, i) => (
                    <p key={i}>{text}</p>
                  ))}
                </div>
              ))}
              
              <div ref={storiesEndRef} />
              
              {error && <div className="error-card fade-in">⚠️ {error}</div>}
              
              <div className="glass-panel continue-panel fade-in delay">
                <ContinueForm onSubmit={handleContinue} loading={loading} />
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
