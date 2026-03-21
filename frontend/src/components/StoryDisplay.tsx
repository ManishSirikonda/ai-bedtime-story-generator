export default function StoryDisplay({ story }: { story: string }) {
    // LangGraph might return newlines (\n), so we map them to <p> tags for nice formatting
    const paragraphs = story.split("\n").filter(p => p.trim() !== "");

    return (
        <div className="story-card">
            {paragraphs.map((text, i) => (
                <p key={i}>{text}</p>
            ))}
        </div>
    );
}
