import React, { useState } from "react";

export default function FloatingChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ from: string; text: string }[]>([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // add user message
    setMessages(prev => [...prev, { from: "user", text: input }]);

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": import.meta.env.VITE_API_KEY,
      },
      body: JSON.stringify({ message: input }),
    });

    const data = await res.json();

    // add bot response
    setMessages(prev => [...prev, { from: "bot", text: data.response }]);

    setInput("");
  };

  return (
    <div className="fixed bottom-6 right-6">
      {isOpen && (
        <div className="bg-white p-4 rounded shadow-lg w-80 h-96 flex flex-col">
          <div className="flex-1 overflow-y-auto">
            {messages.map((m, i) => (
              <div
                key={i}
                className={m.from === "user" ? "text-right mb-2" : "text-left mb-2"}
              >
                <span className="inline-block bg-gray-200 p-2 rounded">
                  {m.text}
                </span>
              </div>
            ))}
          </div>

          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            className="border p-2 w-full mb-2"
          />

          <button
            onClick={sendMessage}
            className="bg-blue-600 text-white p-2 rounded w-full"
          >
            Send
          </button>
        </div>
      )}

      {/* chat button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-blue-600 text-white p-4 rounded-full shadow-lg"
      >
        💬
      </button>
    </div>
  );
}
