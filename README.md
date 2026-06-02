# 🛰️ OrbitSafe

OrbitSafe is a climate monitoring system developed as a college project for the **Global Solution 2026** challenge at **FIAP — Engenharia de Software, 1st year**.

The challenge theme was the space industry, so we built a platform that uses satellite data from NASA and INPE to monitor wildfire and flood risks across Brazilian regions in real time.

---

## 💡 What it does

The system calculates an **OrbitSafe Risk Index (IRO)** — a value from 0 to 100 — based on temperature, humidity, and regional historical data. When the IRO reaches critical levels, the system triggers automatic alerts.

Climate data is fetched automatically in real time via the **CPTEC/INPE API** (Brazil's national weather service). If CPTEC is unavailable, the system falls back to **wttr.in**.

---

## 🖥️ Features

- Register Brazilian regions for monitoring (validated against all 27 states)
- Automatically fetch real-time temperature and humidity via API
- Calculate the IRO for any registered region
- View alert history with filters
- Generate a full risk report sorted by danger level

---

## 🚀 How to run

Install the required dependency:

```bash
pip install requests
```

Then run:

```bash
python orbitsafe.py
```

> Requires Python 3.10 or higher (uses `match-case`).

---

## 📡 Data sources

- **CPTEC/INPE** — primary source for real-time climate data in Brazil
- **wttr.in** — fallback weather service
- **NASA FIRMS / INPE BDQueimadas** — referenced as the scientific basis for the IRO model

---

## 📁 Project structure

```
orbitsafe.py   → main program and menu
funcoes.py     → all functions and logic
```

---

## 👥 Team

Developed by students of Software Engineering at FIAP — São Paulo, Brazil.  
Global Solution 2026 · 1st Semester.