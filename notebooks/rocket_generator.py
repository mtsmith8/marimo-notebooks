import marimo

__generated_with = "0.11.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import numpy as np
    from scipy.signal import find_peaks
    #import matplotlib.pyplot as plt
    import altair as alt
    return alt, find_peaks, mo, np, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Experiment Data Analysis

        Horizontal tube (PVC / Stainless Steel) layout with compressed air propulsion or rocket engine.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.image("v1.PNG", width=700, height=500, caption="V1 PVC Tube Setup")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Test Data""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Data Read-in
        Importing CSV data from the oscilloscope
        """
    )
    return


@app.cell(hide_code=True)
def _(pl):
    df = pl.read_csv('rocket-data/first-rocket.csv')

    df = df.with_columns(
        pl.when(pl.col("Ch1 (V)") == "undefined")
        .then(None)
        .otherwise(pl.col("Ch1 (V)").cast(pl.Float64, strict=False))
        .alias("Ch1 (V)")
    )

    df = df.rename({"Ch1 (V)": "V"})
    df = df.drop_nulls()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Plotting the Waveform Data""")
    return


@app.cell(hide_code=True)
def _(alt, df, mo):
    chart = mo.ui.altair_chart(alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Time (s):Q', title="Seconds (s)"),
        y=alt.Y('V:Q', title="Volts (V)")
    ).properties(
        title="Voltage (V) vs Time (s)"
    ))

    chart
    return (chart,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Data Analysis

        Descriptive statistics, Peak-to-Peak Voltage, and RMS voltage
        """
    )
    return


@app.cell(hide_code=True)
def _(df, np, pl):
    stats = df.select([
            pl.col("V").min().alias("min"),
            pl.col("V").max().alias("max"),
            pl.col("V").mean().alias("mean"),
            pl.col("V").std().alias("std")
    ])
    print("Voltage Statistics:")
    print(stats)

    min_voltage = df.select(pl.col("V").min()).item()
    max_voltage = df.select(pl.col("V").max()).item()
    peak_to_peak = max_voltage - min_voltage

    print(f"Peak-to-Peak Voltage: {peak_to_peak} V")

    # RMS voltage gives an effective voltage value similar to a DC voltage delivering the same power.
    rms_sq = df.select((pl.col("V") ** 2).mean().alias("mean_square")).item()
    rms_voltage = np.sqrt(rms_sq)
    print(f"RMS Voltage: {rms_voltage} V")
    return max_voltage, min_voltage, peak_to_peak, rms_sq, rms_voltage, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Power Measurements
        Extract power output from rectified test setup
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        $P = V^2 / R$

        Impedance matching revealed 1.1 ohm load is optimal. 

        Using a 20:1 voltage divider, so all voltages are multiplied by 21.
        """
    )
    return


@app.cell
def _(df, np):
    # Extract arrays for time and voltage
    time = df["Time (s)"].to_numpy()
    voltage = df["V"].to_numpy()
    resistance = 1.1  # ohms
    v_divider = 21 # 20:1 ratio

    # --- Power Calculations ---
    power = v_divider * voltage**2 / resistance
    avg_power = np.mean(power)
    max_power = np.max(power)
    v_pp = np.max(voltage) - np.min(voltage)
    v_rms = np.sqrt(np.mean(voltage ** 2))

    print("Power Statistics:")
    print(f"  Average Power        : {avg_power:.5f} W")
    print(f"  Max Instantaneous    : {max_power:.5f} W")
    print(f"  Peak-to-Peak Voltage : {v_pp:.5f} V")
    print(f"  RMS Voltage          : {v_rms:.5f} V")
    return (
        avg_power,
        max_power,
        power,
        resistance,
        time,
        v_divider,
        v_pp,
        v_rms,
        voltage,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Velocity Calculations
        Extract data to calculate velocity of the bullet passing through the tube
        """
    )
    return


@app.cell
def _(find_peaks, time, voltage):
    # --- Detect voltage peaks (first peak from each coil pulse) ---
    # Threshold and distance tuned for this waveform shape
    peaks, _ = find_peaks(
        voltage,
        height=0.1,        # increase to ignore small peaks
        distance=100,      # increase to enforce spacing
        prominence=0.05    # increase to require sharper peaks
    )

    rocket_mass = 190 # g

    # Extract times of the peaks
    peak_times = time[peaks]

    # Ensure we found enough peaks
    if len(peak_times) >= 2:
        t_first = peak_times[0] # first coil peak
        t_second = peak_times[3] # second coil peak
        delta_t = t_second - t_first
        coil_spacing = 0.59  # meters between two coils
        velocity = coil_spacing / delta_t

        print("Velocity Estimate from 4-Coil Peaks (based on two peaks chosen):")
        print(f"  Peak Times (s)        : {peak_times[:].round(6)}")
        print(f"  Time Between Peaks    : {delta_t:.6f} s")
        print(f"  Coil Spacing          : {coil_spacing:.3f} m")
        print(f"  Estimated Speed       : {velocity:.2f} m/s")
    else:
        print("Not enough peaks found to estimate velocity.")
    return (
        coil_spacing,
        delta_t,
        peak_times,
        peaks,
        rocket_mass,
        t_first,
        t_second,
        velocity,
    )


@app.cell
def _(mo):
    mo.md(r"""## Notes""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Notes on Future Versions

        """
    )
    return


if __name__ == "__main__":
    app.run()
