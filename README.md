🔥 Python based Automatic Fire Detection & Suppression System

 Code in Place — Final Project 




## What it does

A Python console program that simulates an embedded fire-safety controller.  
It reads dual sensor data (smoke level + temperature), averages 5 readings, and classifies the environment:

| Condition | Trigger | Response |
|-----------|---------|----------|
| 🔥 Fire | Smoke ≥ 70 ppm and Temp ≥ 60 °C | CO₂ extinguisher + fan + alarm — loops until safe |
| 💨 Gas leak | Smoke ≥ 70 ppm (temp normal) | Exhaust fan + alarm — loops until smoke clears |
| ✅ All clear | Both below threshold | Standby |

The suppression cycle uses a `while` loop — the system keeps running until conditions drop to safe levels, not for a fixed time.



## Author

Arian — undergraduate engineering student, IUT Dhaka  
Code in Place (Stanford University) — 2025
