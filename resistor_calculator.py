# RESISTOR COMBINATION CALCULATOR
# Calculates total resistance in series and in parallel.
# My own twist: it accepts values like 4.7k or 2M, and it also uses a
# supply voltage to work out current, voltage drop and power (Ohm's law).


# ---------- INPUT HELPERS ----------

def parse_resistance(text):
    """Convert text like '470', '4.7k' or '2M' into ohms (a float).
    Raises ValueError if the text is not a valid number."""
    text = text.strip().replace("ohms", "").replace("ohm", "").strip()
    multiplier = 1
    if text.endswith(("k", "K")):      # k = kilo (x 1,000)
        multiplier = 1000
        text = text[:-1]
    elif text.endswith("M"):           # M = mega (x 1,000,000)
        multiplier = 1000000
        text = text[:-1]
    return float(text) * multiplier    # float() raises ValueError if invalid


def get_resistor_count():
    """Keep asking until the user enters a whole number of at least 2."""
    while True:
        try:
            count = int(input("How many resistors do you have? "))
        except ValueError:
            print("  Please type a whole number, e.g. 3.")
            continue
        if count < 2:
            print("  You need at least 2 resistors to combine them.")
        else:
            return count


def get_resistor_value(position):
    """Keep asking until the user enters a valid positive resistance."""
    while True:
        try:
            value = parse_resistance(input(f"  Resistor {position} (e.g. 470, 4.7k, 2M): "))
        except ValueError:
            print("  Invalid value. Try something like 470, 4.7k or 2M.")
            continue
        if value <= 0:
            print("  Resistance must be greater than zero.")
        else:
            return value


def get_voltage():
    """Keep asking until the user enters a valid positive supply voltage."""
    while True:
        try:
            voltage = float(input("Supply voltage in volts (e.g. 12): "))
        except ValueError:
            print("  Please type a number, e.g. 9 or 12.5.")
            continue
        if voltage <= 0:
            print("  Voltage must be greater than zero.")
        else:
            return voltage


# ---------- CALCULATIONS ----------

def series_total(values):
    """Series: R_total = R1 + R2 + ..."""
    total = 0
    for r in values:
        total += r
    return total


def parallel_total(values):
    """Parallel: 1/R_total = 1/R1 + 1/R2 + ..."""
    inverse_sum = 0
    for r in values:
        inverse_sum += 1 / r
    return 1 / inverse_sum


def format_ohms(value):
    """Show ohms neatly: 4700 -> '4.7 kOhm'."""
    if value >= 1000000:
        return f"{value / 1000000:.4g} MOhm"
    elif value >= 1000:
        return f"{value / 1000:.4g} kOhm"
    else:
        return f"{value:.4g} Ohm"


def show_ohms_law(voltage, resistance, label):
    """Print current and power for a given total resistance."""
    current = voltage / resistance        # I = V / R
    power = voltage * current             # P = V x I
    print(f"  {label}: I = {current * 1000:.4g} mA, P = {power * 1000:.4g} mW")


# ---------- MAIN PROGRAM ----------

def main():
    print("=== RESISTOR COMBINATION CALCULATOR ===\n")
    while True:
        count = get_resistor_count()
        resistors = []                                  # list of all values
        for i in range(1, count + 1):
            resistors.append(get_resistor_value(i))

        r_series = series_total(resistors)
        r_parallel = parallel_total(resistors)

        print("\n--- RESULTS ---")
        print("Series total   :", format_ohms(r_series))
        print("Parallel total :", format_ohms(r_parallel))

        # Twist: Ohm's law with a supply voltage
        voltage = get_voltage()
        print(f"\nAt {voltage:g} V:")
        show_ohms_law(voltage, r_series, "Series  ")
        show_ohms_law(voltage, r_parallel, "Parallel")

        # In series, the same current flows, so each drop is I x R
        current = voltage / r_series
        print("  Voltage drop across each resistor in series:")
        for i, r in enumerate(resistors, start=1):
            print(f"    R{i} ({format_ohms(r)}): {current * r:.4g} V")

        again = input("\nCalculate another set? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


# This line actually STARTS the program. Without it, nothing runs.
main()
