# 🤖 CodeAlpha FAQ Chatbot

An AI-powered FAQ Chatbot built using **React, Flask, NLTK, TF-IDF, and Cosine Similarity**.

The chatbot understands user questions, preprocesses them using Natural Language Processing, finds the most relevant FAQ from its knowledge base, and returns the best matching answer.

---

## ✨ Features

- 🤖 AI-powered FAQ chatbot
- 🧠 Natural Language Processing using NLTK
- 🔤 Text tokenization using NLTK
- 🌱 Stemming using Porter Stemmer
- 🛑 Stop-word removal
- 📊 TF-IDF based text vectorization
- 📐 Cosine Similarity for FAQ matching
- 💬 Interactive chatbot interface
- ⚡ Quick question suggestions
- ⌨️ Enter key support for sending messages
- 📝 Shift + Enter for multi-line messages
- 📊 Matching confidence display
- 🔄 Clear chat functionality
- 📱 Responsive design
- 🚫 Fallback response for unsupported questions

---

## 🧠 How It Works

The chatbot follows a Natural Language Processing pipeline to understand and match user questions.

```text
User Question
      ↓
Text Preprocessing
      ↓
NLTK Tokenization
      ↓
Stop-word Removal
      ↓
Stemming
      ↓
TF-IDF Vectorization
      ↓
Cosine Similarity
      ↓
Best Matching FAQ
      ↓
Chatbot Response