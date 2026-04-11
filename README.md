# AI Security RAG Lab

A structured AI-powered security knowledge retrieval system that combines lexical and semantic search to provide accurate explanations for vulnerabilities, attack patterns, techniques, and security concepts.

---

## Overview

This project is a mini security knowledge assistant built with:

- Structured JSON-based knowledge base
- Hybrid retrieval (lexical + semantic search)
- Type-aware answer generation
- CLI-based interactive interface

It is designed to simulate how modern AI-assisted security tools retrieve and explain knowledge.

---

## Features

- Hybrid search:
  - Keyword-based matching
  - Embedding-based semantic similarity
- Type-aware responses:
  - `vulnerability`
  - `attack`
  - `technique`
  - `topic`
- AI-style explanation output
- Confidence scoring
- Modular Python architecture

---

## Project Structure

```bash
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
