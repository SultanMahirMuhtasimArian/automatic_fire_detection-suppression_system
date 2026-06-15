'''
Automatic Fire Detection and Suppression System
================================================
Author  : Arian

'''


import time

# ── Constants (safety thresholds) ─────────────────────────────────────────────
SMOKE_FIRE_THRESHOLD   = 70   # ppm  – both exceeded → fire
TEMP_FIRE_THRESHOLD    = 60   # °C   – both exceeded → fire
SMOKE_GAS_THRESHOLD    = 70   # ppm  – only smoke high → gas leak
SAFE_TEMP              = 35   # °C   – extinguisher keeps running until below this
SAFE_SMOKE             = 30   # ppm  – fan keeps running until below this
READINGS_COUNT         = 5    # number of sensor samples to average

# ── Visual helpers ─────────────────────────────────────────────────────────────
DIVIDER = "=" * 55
THIN    = "-" * 55


def print_header():
    print(DIVIDER)
    print("   AUTOMATIC FIRE DETECTION & SUPPRESSION SYSTEM")
    print("   Dedicated to the victims of Bailey Road, 2024")
    print(DIVIDER)


def print_status(label, value, unit=""):
    print(f"  {label:<25} : {value} {unit}")


# ── Core logic ─────────────────────────────────────────────────────────────────

def average(readings):
    """Return the integer average of a list of numbers."""
    total = 0
    for reading in readings:
        total = total + reading
    return total // len(readings)


def classify(avg_smoke, avg_temp):
    """
    Return a string describing the current condition:
      'FIRE'     – both smoke and temp above thresholds
      'GAS_LEAK' – only smoke above threshold
      'CLEAR'    – all normal
    """
    if avg_smoke > SMOKE_FIRE_THRESHOLD and avg_temp > TEMP_FIRE_THRESHOLD:
        return "FIRE"
    elif avg_smoke > SMOKE_GAS_THRESHOLD:
        return "GAS_LEAK"
    else:
        return "CLEAR"


def show_sensor_report(avg_smoke, avg_temp):
    print(THIN)
    print("  SENSOR READINGS (averaged over 5 samples)")
    print(THIN)
    smoke_bar = build_bar(avg_smoke, 100)
    temp_bar  = build_bar(avg_temp, 100)
    print(f"  Smoke Level : {avg_smoke:>3} ppm  [{smoke_bar}]")
    print(f"  Temperature : {avg_temp:>3} °C   [{temp_bar}]")
    print(THIN)


def build_bar(value, max_value, width=20):
    """Return a simple ASCII progress bar string."""
    filled = int((value / max_value) * width)
    filled = min(filled, width)
    return "#" * filled + "." * (width - filled)


def handle_fire(avg_temp, avg_smoke):
    """Fire suppression routine – loops until temp and smoke drop."""
    print()
    print("  !! FIRE DETECTED !!")
    print("  >> CO₂ Extinguisher  : ON")
    print("  >> Exhaust Fan       : ON")
    print("  >> Alarm             : ON")
    print()

    cycle = 1
    current_temp  = avg_temp
    current_smoke = avg_smoke

    while current_temp > SAFE_TEMP or current_smoke > SAFE_SMOKE:
        bar_t = build_bar(current_temp,  100)
        bar_s = build_bar(current_smoke, 100)
        print(f"  [Cycle {cycle:>2}] Spraying CO₂  |  "
              f"Temp: {current_temp:>3}°C [{bar_t}]  |  "
              f"Smoke: {current_smoke:>3} [{bar_s}]")
        # Simulate suppression: each cycle lowers both readings
        current_temp  = current_temp  - 5
        current_smoke = current_smoke - 8
        cycle += 1

    print()
    print("  >> Temperature & smoke within safe limits.")
    print("  >> CO₂ Extinguisher  : OFF")
    print("  >> Exhaust Fan       : OFF")
    print("  >> Alarm             : OFF")
    print("  >> System returning to standby.")


def handle_gas_leak(avg_smoke):
    """Gas-leak ventilation routine – loops until smoke clears."""
    print()
    print("  !! GAS LEAK DETECTED !!")
    print("  >> Exhaust Fan : ON")
    print("  >> Alarm       : ON")
    print("  >> Extinguisher: STANDBY (no active fire)")
    print()

    current_smoke = avg_smoke
    cycle = 1

    while current_smoke > SAFE_SMOKE:
        bar_s = build_bar(current_smoke, 100)
        print(f"  [Cycle {cycle:>2}] Ventilating  |  Smoke: {current_smoke:>3} ppm [{bar_s}]")
        current_smoke = current_smoke - 10
        cycle += 1

    print()
    print("  >> Smoke level safe. Fan OFF. Alarm OFF.")
    print("  >> System returning to standby.")


def handle_clear():
    print()
    print("  >> ALL CLEAR – No threat detected.")
    print("  >> System on standby.")


# ── Modes ──────────────────────────────────────────────────────────────────────

def run_demo_mode():
    """Three pre-built scenarios that showcase every code path."""
    scenarios = [
        {
            "name"      : "Scenario 1 – Active Fire",
            "smoke"     : [85, 90, 88, 87, 92],
            "temp"      : [65, 70, 68, 72, 66],
        },
        {
            "name"      : "Scenario 2 – Gas Leak (No Fire)",
            "smoke"     : [80, 75, 82, 78, 79],
            "temp"      : [28, 30, 29, 27, 31],
        },
        {
            "name"      : "Scenario 3 – All Clear",
            "smoke"     : [10, 12, 11, 9, 13],
            "temp"      : [24, 25, 23, 26, 24],
        },
    ]

    for s in scenarios:
        print()
        print(DIVIDER)
        print(f"  {s['name']}")
        print(DIVIDER)

        avg_smoke = average(s["smoke"])
        avg_temp  = average(s["temp"])
        show_sensor_report(avg_smoke, avg_temp)

        condition = classify(avg_smoke, avg_temp)

        if condition == "FIRE":
            handle_fire(avg_temp, avg_smoke)
        elif condition == "GAS_LEAK":
            handle_gas_leak(avg_smoke)
        else:
            handle_clear()

        print()
        input("  Press ENTER to run next scenario...")


def get_readings_from_user(sensor_name):
    """Prompt user to enter READINGS_COUNT values; return them as a list."""
    readings = []
    print(f"\n  Enter {READINGS_COUNT} {sensor_name} readings (one per line):")
    count = 1
    while count <= READINGS_COUNT:
        raw = input(f"    Reading {count}: ").strip()
        try:
            value = int(raw)
            if value < 0:
                print("    Value must be 0 or above. Try again.")
            else:
                readings.append(value)
                count += 1
        except ValueError:
            print("    Please enter a whole number.")
    return readings


def run_interactive_mode():
    """User types their own sensor readings and sees the system react."""
    print()
    print("  INTERACTIVE MODE")
    print("  Enter your own sensor data to test the system.")
    print(THIN)
    print("  Thresholds for reference:")
    print(f"    Smoke ≥ {SMOKE_FIRE_THRESHOLD} ppm  AND  Temp ≥ {TEMP_FIRE_THRESHOLD}°C  →  FIRE")
    print(f"    Smoke ≥ {SMOKE_GAS_THRESHOLD} ppm  (temp ok)         →  GAS LEAK")
    print(f"    Below both thresholds               →  ALL CLEAR")
    print()

    while True:
        smoke_list = get_readings_from_user("smoke (ppm)")
        temp_list  = get_readings_from_user("temperature (°C)")

        avg_smoke = average(smoke_list)
        avg_temp  = average(temp_list)
        show_sensor_report(avg_smoke, avg_temp)

        condition = classify(avg_smoke, avg_temp)

        if condition == "FIRE":
            handle_fire(avg_temp, avg_smoke)
        elif condition == "GAS_LEAK":
            handle_gas_leak(avg_smoke)
        else:
            handle_clear()

        print()
        again = input("  Test another set of readings? (y / n): ").strip().lower()
        if again != "y":
            break


# ── Log (added feature: history tracking) ─────────────────────────────────────

log = []       # list of dicts – each entry is one scan result

def log_result(avg_smoke, avg_temp, condition):
    """Append a scan result to the in-memory log."""
    entry = {
        "smoke"    : avg_smoke,
        "temp"     : avg_temp,
        "condition": condition,
    }
    log.append(entry)


def show_log():
    """Print all recorded scan results."""
    if len(log) == 0:
        print("  No scans recorded yet.")
        return

    print()
    print(f"  {'#':<4} {'Smoke':>7} {'Temp':>6}   Condition")
    print(THIN)
    index = 1
    for entry in log:
        print(f"  {index:<4} {entry['smoke']:>5} ppm  {entry['temp']:>4}°C   {entry['condition']}")
        index += 1


# ── Main menu ──────────────────────────────────────────────────────────────────

def main():
    print_header()

    while True:
        print()
        print("  MAIN MENU")
        print(THIN)
        print("  1. Run demo (3 built-in scenarios)")
        print("  2. Enter your own sensor readings")
        print("  3. View scan history")
        print("  4. About this project")
        print("  5. Exit")
        print(THIN)

        choice = input("  Choose (1-5): ").strip()

        if choice == "1":
            run_demo_mode()

        elif choice == "2":
            run_interactive_mode()

        elif choice == "3":
            show_log()

        elif choice == "4":
            print()
            print(DIVIDER)
            print("  ABOUT")
            print(DIVIDER)
            print("  Project : Automatic Fire Detection & Suppression")
            print("  Author  : Arian  |  Code in Place – Final Project")
            print()
            print("  This system simulates a dual-sensor fire-safety")
            print("  controller. It averages smoke (ppm) and temperature")
            print("  (°C) readings, then classifies the environment as")
            print("  FIRE, GAS LEAK, or ALL CLEAR and responds with")
            print("  the appropriate countermeasures.")
            print()
            print("  Dedicated to the victims of the Bailey Road fire,")
            print("  Dhaka, February 2024.")
            print(DIVIDER)

        elif choice == "5":
            print()
            print("  System shutdown. Stay safe.")
            print(DIVIDER)
            break

        else:
            print("  Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
