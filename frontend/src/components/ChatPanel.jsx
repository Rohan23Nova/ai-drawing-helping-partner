import { useState } from "react";

const promptLabels = [
  "What should I draw first?",
  "How do I check proportions?",
  "What should I focus on next?",
  "Are my shapes positioned correctly?"
];

export default function ChatPanel({
  messages,
  onSendMessage,
  isLoading,
  error,
  currentStepTitle
}) {
  const [draft, setDraft] = useState("");

  async function submitMessage(nextMessage = draft) {
    const trimmed = nextMessage.trim();
    if (!trimmed || isLoading) {
      return;
    }

    const sent = await onSendMessage(trimmed);
    if (sent) {
      setDraft("");
    }
  }

  return (
    <section className="workspace-card chat-card">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Drawing Partner</p>
          <h3>Ask about your current step{currentStepTitle ? `: ${currentStepTitle}` : ""}</h3>
          <p className="section-subcopy">
            Keep questions specific so the feedback stays useful while you work.
          </p>
        </div>
      </div>

      <div className="quick-prompts" aria-label="Suggested prompts">
        {promptLabels.map((prompt) => (
          <button
            key={prompt}
            type="button"
            className="prompt-chip"
            onClick={() => submitMessage(prompt)}
            disabled={isLoading}
          >
            {prompt}
          </button>
        ))}
      </div>

      <div className="chat-thread" aria-live="polite">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <strong>No conversation yet.</strong>
            <p>Ask for help with placement, structure, confidence, or what to do next.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <article
              key={`${message.role}-${index}`}
              className={`chat-message ${message.role === "user" ? "is-user" : "is-assistant"}`}
            >
              <p className="chat-role">{message.role === "user" ? "You" : "Partner"}</p>
              <p>{message.content}</p>
            </article>
          ))
        )}

        {isLoading ? (
          <div className="chat-message is-assistant is-loading">
            <p className="chat-role">Partner</p>
            <p>Thinking through your drawing...</p>
          </div>
        ) : null}
      </div>

      <form
        className="chat-form"
        onSubmit={(event) => {
          event.preventDefault();
          submitMessage();
        }}
      >
        <label className="sr-only" htmlFor="chat-input">
          Ask your drawing partner
        </label>
        <textarea
          id="chat-input"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Ask about the current step, proportions, or what to simplify."
          rows={3}
          disabled={isLoading}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              submitMessage();
            }
          }}
        />
        <div className="chat-submit">
          {error ? (
            <p className="chat-error" role="alert">
              Something went wrong. Your drawing data is still safe.
            </p>
          ) : (
            <span className="chat-helper">Enter to send, Shift+Enter for a new line.</span>
          )}
          <button type="submit" className="primary-button" disabled={!draft.trim() || isLoading}>
            Send
          </button>
        </div>
      </form>
    </section>
  );
}
