const BASE = "http://localhost:8000";

export async function generateStory(theme: string, sessionId?: string) {
    const res = await fetch(`${BASE}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ theme, session_id: sessionId }),
    });
    return res.json();
}

export async function continueStory(sessionId: string, feedback: string) {
    const res = await fetch(`${BASE}/api/continue`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, feedback }),
    });
    return res.json();
}
