import { useState } from "react";

export default function ContinueForm({ onSubmit, loading }: {
    onSubmit: (feedback: string) => void;
    loading: boolean;
}) {
    const [feedback, setFeedback] = useState("");

    return (
        <form className="input-form continue-form" onSubmit={(e) => { e.preventDefault(); onSubmit(feedback); setFeedback(""); }}>
            <input
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Add a story beat…"
                disabled={loading}
            />
            <button type="submit" disabled={loading || !feedback.trim()}>
                {loading ? "Writing…" : "Continue"}
            </button>
        </form>
    );
}
