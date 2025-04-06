# 🗼 XRPL FastAPI Service — Paris Blockchain Week 2025 Hackathon

Welcome to the XRPL FastAPI project, developed for [Paris Blockchain Week 2025 Hackathon](https://www.parisblockchainweek.com/hackathon-2025)! 🇫🇷

This project leverages **FastAPI** to expose high-performance REST APIs powered by the **XRP Ledger (XRPL)**. It provides an easy interface for developers, dApps, and enterprises to interact with the decentralized XRPL ecosystem.

---

## 🚀 Features

- 🔗 XRPL integration for wallet creation, balance checks, and transaction submissions  
- ⚡ FastAPI backend for high-speed REST API delivery

---

## 📦 Tech Stack

- **Python 3.13.1+**  
- **FastAPI**  
- **XRPL-Py**

---

## ⚙️ Installation

### Prerequisites

- Python 3.13.1+

### Clone & Install

```bash
git clone https://github.com/CloviusIX/pbw-hackathon-2025.git
source .venv/bin/activate
make
```

### Run

```bash
make run
```

### Environment Setup

Create a `.env` file at the root:

```env
XRPL_NODE=https://s.altnet.rippletest.net:51234
```