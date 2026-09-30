import { useState, useRef, useEffect } from "react";
import "./App.css";

const BACKEND_URL = "http://127.0.0.1:5002";

const quickQuestions = [
  "What is FAQBot AI?",
  "What can you help me with?",
  "How can I reset my password?",
  "What are the admission requirements?",
  "How can I register for placements?",
  "What are the library timings?",
];

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text: "Hello! 👋 I'm FAQBot AI. Ask me anything about admissions, courses, fees, exams, placements, library, hostel, or technical support.",
      confidence: null,
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async (messageText = input) => {
    const question = messageText.trim();

    if (!question || loading) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      text: question,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(
        `${BACKEND_URL}/api/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: question,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || "Unable to get response."
        );
      }

      const botMessage = {
        id: Date.now() + 1,
        type: "bot",
        text: data.answer,
        confidence: data.confidence,
        matchedQuestion: data.matched_question,
      };

      setMessages((previous) => [
        ...previous,
        botMessage,
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          type: "error",
          text:
            "Sorry, I couldn't connect to the FAQBot AI server. Please make sure the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);

      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage();
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: Date.now(),
        type: "bot",
        text: "Chat cleared! 👋 Ask me a new question whenever you're ready.",
        confidence: null,
      },
    ]);

    setInput("");
    inputRef.current?.focus();
  };

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-icon">AI</div>

          <div>
            <h1>FAQBot AI</h1>
            <p>Intelligent FAQ Assistant</p>
          </div>
        </div>

        <div className="online-status">
          <span className="status-dot"></span>
          AI Assistant Online
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div className="badge">
            ✦ AI POWERED FAQ CHATBOT
          </div>

          <h2>
            Get answers
            <span> instantly.</span>
          </h2>

          <p>
            Ask questions in natural language and get
            relevant answers from our intelligent FAQ
            knowledge base.
          </p>
        </section>

        <section className="chat-card">
          <div className="chat-header">
            <div className="bot-profile">
              <div className="bot-avatar">🤖</div>

              <div>
                <h3>FAQBot AI</h3>
                <span>
                  <span className="small-dot"></span>
                  Ready to answer
                </span>
              </div>
            </div>

            <button
              className="clear-chat"
              onClick={clearChat}
              disabled={loading}
              title="Clear conversation"
            >
              🗑 Clear Chat
            </button>
          </div>

          <div className="chat-body">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message-row ${message.type}`}
              >
                {message.type === "bot" && (
                  <div className="message-avatar">
                    🤖
                  </div>
                )}

                {message.type === "error" && (
                  <div className="message-avatar error-avatar">
                    ⚠
                  </div>
                )}

                <div className="message-content">
                  <div className="message-label">
                    {message.type === "user"
                      ? "You"
                      : message.type === "error"
                      ? "System"
                      : "FAQBot AI"}
                  </div>

                  <div className="message-bubble">
                    {message.text}
                  </div>

                  {message.confidence !== null &&
                    message.confidence !== undefined && (
                      <div className="confidence">
                        <span>
                          Match confidence:
                        </span>

                        <strong>
                          {message.confidence}%
                        </strong>
                      </div>
                    )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row bot">
                <div className="message-avatar">
                  🤖
                </div>

                <div className="message-content">
                  <div className="message-label">
                    FAQBot AI
                  </div>

                  <div className="message-bubble typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef}></div>
          </div>

          <div className="quick-section">
            <div className="quick-title">
              <span>⚡</span>
              Quick Questions
            </div>

            <div className="quick-buttons">
              {quickQuestions.map((question) => (
                <button
                  key={question}
                  onClick={() =>
                    sendMessage(question)
                  }
                  disabled={loading}
                >
                  {question}
                </button>
              ))}
            </div>
          </div>

          <form
            className="input-area"
            onSubmit={handleSubmit}
          >
            <textarea
              ref={inputRef}
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Type your question here..."
              rows="1"
              maxLength="500"
              disabled={loading}
            />

            <div className="input-bottom">
              <span>
                {input.length}/500
              </span>

              <button
                className="send-button"
                type="submit"
                disabled={!input.trim() || loading}
              >
                {loading ? "Thinking..." : "Send ✦"}
              </button>
            </div>
          </form>

          <div className="chat-hint">
            Press <strong>Enter</strong> to send •{" "}
            <strong>Shift + Enter</strong> for a new line
          </div>
        </section>

        <section className="features">
          <div className="feature">
            <div className="feature-icon">🧠</div>

            <div>
              <h3>NLP Powered</h3>
              <p>
                Understands natural language questions.
              </p>
            </div>
          </div>

          <div className="feature">
            <div className="feature-icon">🎯</div>

            <div>
              <h3>Smart Matching</h3>
              <p>
                Uses TF-IDF and cosine similarity.
              </p>
            </div>
          </div>

          <div className="feature">
            <div className="feature-icon">⚡</div>

            <div>
              <h3>Instant Answers</h3>
              <p>
                Get relevant FAQ answers quickly.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <p>
          FAQBot AI • Intelligent FAQ Chatbot
        </p>
      </footer>
    </div>
  );
}

export default App;