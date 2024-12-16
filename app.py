import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import collections.abc #에러가나면, 한줄 띄거나 붙이거나 해서 새로고침하기

# Import collections.abc safely based on Python version
if sys.version_info >= (3, 10):
    from collections.abc import Iterable
else:
    from collections import Iterable

def calculate_y_fit(a, b, c, x):
    return a * (1 - np.exp(-b * (x ** c)))

def plot_reach_curve(target_data, target):
    """Plots the reach curve for a given target."""
    plt.figure(figsize=(10, 6))

    # Group data by reach항목 and plot each
    reach_items = target_data['reach항목'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(reach_items)))  # Assign distinct colors per reach_item

    for color, reach_item in zip(colors, reach_items):
        item_data = target_data[target_data['reach항목'] == reach_item]
        for _, row in item_data.iterrows():
            segment_condition = row['Segment']
            if "≤" in segment_condition:
                max_grp = int(segment_condition.split("≤")[-1].strip())
                x = np.linspace(0, max_grp, 300)
            elif ">" in segment_condition:
                min_grp = int(segment_condition.split(">")[-1].strip())
                x = np.linspace(min_grp, 3000, 300)
            else:
                x = np.linspace(0, 3000, 300)  # Default range if no condition

            y_fit = calculate_y_fit(row['A'], row['B'], row['C'], x)
            label = f"{reach_item} - {row['Segment']}"
            plt.plot(x, y_fit, label=label, color=color)

    plt.title(f"Reach Curve for {target}")
    plt.xlabel("GRP")
    plt.ylabel("Reach (%)")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Streamlit app
st.title("Reach Curve Visualizer")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Load data
    data = pd.read_csv(uploaded_file)

    # User input for target selection
    targets = data['Target'].unique()
    selected_target = st.selectbox("Select Target", targets)

    # Filter data by selected target
    target_data = data[data['Target'] == selected_target]

    # Plot reach curve
    plot_reach_curve(target_data, selected_target)

    st.success("Reach curve plotted successfully!")

# Part.2 TV KPI simulation / Budgeting system
st.header("Part.2 TV KPI Simulation / Budgeting System")

# Step 1: User input for CPRP
cprp_input = st.text_input("Enter Expected CPRP (in 1,000 KRW)", value="1,000")
cprp_input = cprp_input.replace(",", "")
try:
    cprp_value = int(cprp_input) * 1000  # Convert to KRW
except ValueError:
    st.error("Please enter a valid numeric value for CPRP.")
    cprp_value = None

# Step 2: User input for Budget
budget_input = st.text_input("Enter Planned Budget (in 1,000 KRW)", value="10,000")
budget_input = budget_input.replace(",", "")
try:
    budget_value = int(budget_input) * 1000  # Convert to KRW
except ValueError:
    st.error("Please enter a valid numeric value for Budget.")
    budget_value = None

# Step 3: Reconstruct the reach curve with Budget as X-axis
if cprp_value and budget_value:
    def plot_budget_curve(target_data, target, cprp):
        """Plots the reach curve with Budget as the X-axis."""
        plt.figure(figsize=(10, 6))

        reach_items = target_data['reach항목'].unique()
        colors = plt.cm.tab10(np.linspace(0, 1, len(reach_items)))

        for color, reach_item in zip(colors, reach_items):
            item_data = target_data[target_data['reach항목'] == reach_item]
            for _, row in item_data.iterrows():
                segment_condition = row['Segment']
                if "≤" in segment_condition:
                    max_grp = int(segment_condition.split("≤")[-1].strip())
                    x_grp = np.linspace(0, max_grp, 300)
                elif ">" in segment_condition:
                    min_grp = int(segment_condition.split(">")[-1].strip())
                    x_grp = np.linspace(min_grp, 3000, 300)
                else:
                    x_grp = np.linspace(0, 3000, 300)

                x_budget = x_grp * cprp / 1000  # Convert GRP to Budget in 1,000 KRW
                y_fit = calculate_y_fit(row['A'], row['B'], row['C'], x_grp)
                label = f"{reach_item} - {row['Segment']}"
                plt.plot(x_budget, y_fit, label=label, color=color)

        plt.title(f"Budget-based Reach Curve for {target}")
        plt.xlabel("Budget (1,000 KRW)")
        plt.ylabel("Reach (%)")
        plt.legend()
        plt.grid()

        # Format X-axis with commas for thousands
        ax = plt.gca()
        ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

        st.pyplot(plt)

    # Plot budget curve
    plot_budget_curve(target_data, selected_target, cprp_value)

    # Step 4: Summary Table
    plan_grp = budget_value / cprp_value if cprp_value else 0

    # Calculate Reach+ values
    def calculate_reach(grp, reach_items):
        results = {}
        for reach_item in reach_items:
            item_data = target_data[target_data['reach항목'] == reach_item]
            for _, row in item_data.iterrows():
                if grp <= 0:
                    results[reach_item] = "N/A"
                    continue
                segment_condition = row['Segment']
                if "≤" in segment_condition and grp <= int(segment_condition.split("≤")[-1].strip()):
                    results[reach_item] = calculate_y_fit(row['A'], row['B'], row['C'], grp)
                    break
                elif ">" in segment_condition and grp > int(segment_condition.split(">")[-1].strip()):
                    results[reach_item] = calculate_y_fit(row['A'], row['B'], row['C'], grp)
        return results

    reach_results = calculate_reach(plan_grp, ["reach 1+", "reach 3+", "reach 8+"])

    # Calculate Expected A.F
    expected_reach_plus = reach_results.get("reach 1+", "N/A")
    expected_af = plan_grp / expected_reach_plus if expected_reach_plus not in ["N/A", 0] else "N/A"

    # Prepare summary table
    summary_data = {
        "Metric": [
            "Target", 
            "Plan GRP", 
            "CPRP", 
            "Budget (1,000 KRW)", 
            "Expected Reach+", 
            "Expected Reach3+", 
            "Expected Reach8+", 
            "Expected A.F"
        ],
        "Value": [
            selected_target,
            f"{plan_grp:.2f}",
            f"{cprp_value / 1000:,}",
            f"{budget_value / 1000:,}",
            f"{expected_reach_plus:.2f}" if expected_reach_plus != "N/A" else "N/A",
            f"{reach_results.get('reach 3+', 'N/A'):.2f}" if "reach 3+" in reach_results else "N/A",
            f"{reach_results.get('reach 8+', 'N/A'):.2f}" if "reach 8+" in reach_results else "N/A",
            f"{expected_af:.2f}" if expected_af != "N/A" else "N/A"
        ]
    }

    summary_df = pd.DataFrame(summary_data)

    st.subheader("Summary of Calculations")
    st.table(summary_df)

    # Step 5: Plot the third reach curve
    def plot_third_reach_curve(plan_grp, reach_results):
        """Plots the reach curve with Plan GRP as X-axis."""
        x = np.linspace(0, plan_grp * 3, 300)  # X-axis Plan GRP, max = Plan GRP * 3

        plt.figure(figsize=(10, 6))

        # Plot Reach+ curve
        if "reach 1+" in reach_results and reach_results["reach 1+"] != "N/A":
            y_reach_plus = [calculate_y_fit(reach_results["reach 1+"], 0.01, 1, grp) for grp in x]
            plt.plot(x, y_reach_plus, label="Expected Reach+", color="blue")

        # Plot Reach3+ curve
        if "reach 3+" in reach_results and reach_results["reach 3+"] != "N/A":
            y_reach3 = [calculate_y_fit(reach_results["reach 3+"], 0.01, 1, grp) for grp in x]
            plt.plot(x, y_reach3, label="Expected Reach3+", color="green")

        # Plot Reach8+ curve
        if "reach 8+" in reach_results and reach_results["reach 8+"] != "N/A":
            y_reach8 = [calculate_y_fit(reach_results["reach 8+"], 0.01, 1, grp) for grp in x]
            plt.plot(x, y_reach8, label="Expected Reach8+", color="red")

        plt.title("Reach Curve with Plan GRP as X-axis")
        plt.xlabel("Plan GRP")
        plt.ylabel("Reach (%)")
        plt.ylim(0, 100)  # Set Y-axis limits between 0% and 100%
        plt.legend()
        plt.grid()
        st.pyplot(plt)

    plot_third_reach_curve(plan_grp, reach_results)
