import { useState } from "react";

export default function StoryInput({ onSubmit, loading }: {
    onSubmit: (theme: string) => void;
    loading: boolean;
}) {
    const [theme, setTheme] = useState("");

    return (
        <form className="input-form" onSubmit={(e) => { e.preventDefault(); onSubmit(theme); }}>
            <input
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                placeholder="A brave fox who finds a glowing stone…"
                disabled={loading}
            />
            <button type="submit" disabled={loading || !theme.trim()}>
                {loading ? "Generating…" : "Generate Story"}
            </button>
        </form>
    );
}
