# AI Security RAG Lab

A focused AI security project that demonstrates vulnerability retrieval using structured data, hybrid search (lexical + semantic), and AI-style answer generation.

This project is designed to simulate how modern security tools retrieve and explain vulnerabilities using both keyword matching and embedding-based similarity.

---

## 🔍 What This Project Does

* Takes a user query (e.g. `xss`, `prompt injection`)
* Normalizes and processes the input
* Uses **hybrid retrieval**:

  * Lexical scoring (keyword & alias matching)
  * Semantic scoring (sentence-transformers embeddings)
* Combines scores to find the most relevant vulnerability
* Generates a structured, human-readable explanation

---

## ⚙️ Features

* Structured vulnerability dataset (`JSON`)
* Hybrid retrieval (lexical + semantic scoring)
* Precomputed embeddings for performance
* AI-style answer generation layer
* CLI-based interactive interface
* Clean modular Python architecture

---

## 📁 Project Structure

```
ai-security-rag-lab/
├── data/
│   └── vulns.json
├── src/
│   ├── loader.py
│   ├── search.py
│   ├── semantic_search.py
│   └── answer_generator.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 🎯 Current Scope

This tool currently focuses on:

* Web security vulnerabilities
* AI security vulnerabilities

Covered examples:

* SQL Injection (SQLi)
* Cross-Site Scripting (XSS)
* Server-Side Request Forgery (SSRF)
* Remote Code Execution (RCE)
* Broken Access Control
* Prompt Injection
* Indirect Prompt Injection

⚠️ Limitations:

This tool does **not yet cover**:

* Reverse engineering
* Exploit development
* Malware analysis
* Full cybersecurity knowledge domain

The goal is to build a **focused, high-quality retrieval system**, not a general-purpose security assistant.

---

## 🚀 Example Usage

Run the tool:

```bash
python main.py
```

Example interaction:

```
AI Security RAG Lab
Type a query or 'exit' to quit.

Search vulnerability: prompt injection
```

Example output:

```
AI Security Insight for 'prompt injection':

Prompt Injection is the most relevant vulnerability for your query.

What it is:
A vulnerability where an attacker manipulates an AI model through crafted instructions to bypass intended behavior or safety controls.

Why it matters:
This type of vulnerability can be exploited by attackers to compromise system security, steal data, or execute malicious actions.

Common aliases:
prompt injection, llm prompt injection, jailbreak prompt

Basic mitigation:
Use input filtering, instruction separation, output validation, and defense-in-depth prompt design.

Confidence Score: 6.6201
```

---

## 🧠 How It Works

### 1. Input Processing

* Lowercasing
* Normalization
* Alias-aware matching

### 2. Lexical Scoring

* Token overlap
* Alias matching
* Direct keyword signals

### 3. Semantic Scoring

* Sentence embeddings via:

  * `sentence-transformers/all-MiniLM-L6-v2`
* Cosine similarity between query and documents

### 4. Hybrid Ranking

Final score =

```
lexical_score + semantic_score
```

Top results are sorted and returned.

### 5. Answer Generation

A structured response is generated including:

* Description
* Importance
* Aliases
* Mitigation

---

## 🛠️ Installation

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

---

## 📌 Future Improvements

Planned next steps:

* Expand AI security dataset
* Add more vulnerability categories
* Introduce `type` field (vulnerability / topic / technique)
* Improve answer generation (LLM-based reasoning)
* Add simple web UI (Streamlit)
* Add source attribution for responses

---

## 💡 Why This Project Matters

This project demonstrates:

* Practical understanding of **RAG systems**
* Hybrid search design (keyword + semantic)
* Security-focused knowledge modeling
* AI-assisted explanation pipelines
* Real-world thinking: **data quality > model hype**

---

## ⚠️ Disclaimer

This project is for **educational and defensive security purposes only**.

All concepts should be applied only in:

* Authorized lab environments
* CTF competitions
* Bug bounty programs
* Systems you own or have permission to test

---

## 👤 Author

Built as part of a focused journey toward:

* AI Security Engineering
* Bug bounty & vulnerability research
* Real-world offensive security skills

---
