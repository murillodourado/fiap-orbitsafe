# 🛰️ OrbitSafe

OrbitSafe is a climate monitoring system developed as a college project for the **Global Solution 2026** challenge at **FIAP — Engenharia de Software, 1st year**.

The challenge theme was the space industry, so we built a platform that uses satellite data from NASA and INPE to monitor wildfire and flood risks across Brazilian regions in real time.

---

## 💡 What it does

The system calculates an **OrbitSafe Risk Index (IRO)** — a value from 0 to 100 — based on temperature, humidity, and regional historical data. When the IRO reaches critical levels, the system triggers automatic alerts.

---

## 🖥️ Features

- Register regions for monitoring
- Calculate the IRO for any registered region
- View alert history with filters
- Generate a full risk report sorted by danger level

---

## 🚀 How to run

Make sure both files are in the same folder, then run:

```bash
python orbitsafe.py
```

> Requires Python 3.10 or higher (uses `match-case`).

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
