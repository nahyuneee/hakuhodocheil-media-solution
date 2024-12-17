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

# Y_fit 계산 함수
def calculate_y_fit(a, b, c, x):
    return a * (1 - np.exp(-b * (x ** c)))

# Reach Curve 플로팅 함수 (Scatter 중첩 추가)
def plot_reach_curve(target_data, scatter_data, target):
    """기존 리치 커브에 Scatter Plot 추가"""
    plt.figure(figsize=(10, 6))
    
    # Reach 항목별 색상 구분
    reach_items = target_data['reach항목'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(reach_items)))
    
    for color, reach_item in zip(colors, reach_items):
        # 타겟 데이터 필터링
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
                x = np.linspace(0, 3000, 300)
            
            y_fit = calculate_y_fit(row['A'], row['B'], row['C'], x)
            plt.plot(x, y_fit, label=f"{reach_item} - {row['Segment']}", color=color)
    
    # Scatter 데이터 중첩
    scatter_target_data = scatter_data[scatter_data['Target'] == target]
    for reach_item in scatter_target_data['reach항목'].unique():
        scatter_subset = scatter_target_data[scatter_target_data['reach항목'] == reach_item]
        plt.scatter(
            scatter_subset['GRP'], scatter_subset['reach'],
            label=f"Scatter - {reach_item}", alpha=0.7, edgecolor='black'
        )
    
    plt.title(f"Reach Curve with Scatter for {target}")
    plt.xlabel("GRP")
    plt.ylabel("Reach (%)")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Streamlit 앱
st.title("Reach Curve Visualizer with Scatter Plot")

# 첫 번째 파일 업로드 (기존 커브 데이터)
uploaded_file = st.file_uploader("Upload your Reach Curve CSV file", type=["csv"], key="curve_file")

# 두 번째 파일 업로드 (Scatter 데이터)
scatter_file = st.file_uploader("Upload GRP-Reach Scatter CSV file", type=["csv"], key="scatter_file")

if uploaded_file and scatter_file:
    # 파일 로딩
    data = pd.read_csv(uploaded_file)
    scatter_data = pd.read_csv(scatter_file)
    
    # Target 선택
    targets = data['Target'].unique()
    selected_target = st.selectbox("Select Target", targets)
    
    # 타겟 데이터 필터링
    target_data = data[data['Target'] == selected_target]
    
    # 그래프 출력
    plot_reach_curve(target_data, scatter_data, selected_target)
    
    st.success("Reach curve with scatter plotted successfully!")

# 추가된 코드 부분
# KPI Simulation and Budgeting
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

if cprp_value and budget_value:
    # Plan GRP 계산
    plan_grp = budget_value / cprp_value if cprp_value else 0

    # Reach 결과 계산
    def calculate_reach(grp, reach_items, target_data):
        results = {}
        for reach_item in reach_items:
            item_data = target_data[target_data['reach항목'] == reach_item]
            for _, row in item_data.iterrows():
                segment_condition = row['Segment']
                if "≤" in segment_condition and grp <= int(segment_condition.split("≤")[-1].strip()):
                    results[reach_item] = calculate_y_fit(row['A'], row['B'], row['C'], grp)
                    break
                elif ">" in segment_condition and grp > int(segment_condition.split(">")[-1].strip()):
                    results[reach_item] = calculate_y_fit(row['A'], row['B'], row['C'], grp)
        return results

    reach_results = calculate_reach(plan_grp, ["reach 1+", "reach 3+", "reach 8+"], target_data)

    # Summary Table 생성
    expected_reach_plus = reach_results.get("reach 1+", "N/A")
    expected_af = plan_grp / expected_reach_plus if expected_reach_plus not in ["N/A", 0] else "N/A"

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

# 추가2: Summary Table 기반으로 Scatter 그래프 출력 (Expected Reach+ 및 Reach3+ 표기)

def plot_scatter_with_summary(scatter_data, target, plan_grp, expected_reach_plus, expected_reach3):
    """Summary Table 데이터와 동기화된 Scatter Plot만 출력"""
    plt.figure(figsize=(10, 6))
    
    # Scatter 데이터 중첩
    scatter_target_data = scatter_data[scatter_data['Target'] == target]
    for reach_item in scatter_target_data['reach항목'].unique():
        scatter_subset = scatter_target_data[scatter_target_data['reach항목'] == reach_item]
        plt.scatter(
            scatter_subset['GRP'], scatter_subset['reach'],
            label=f"Scatter - {reach_item}", alpha=0.7, edgecolor='black'
        )

    # Summary Table 기반 점 추가
    if expected_reach_plus not in ["N/A", 0]:
        plt.scatter([plan_grp], [expected_reach_plus], color="red", s=150, label="Expected Reach+", marker="X")

    if expected_reach3 not in ["N/A", 0]:
        plt.scatter([plan_grp], [expected_reach3], color="blue", s=150, label="Expected Reach3+", marker="o")

    plt.title(f"Scatter Plot with Summary Data for {target}")
    plt.xlabel("GRP")
    plt.ylabel("Reach (%)")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# 그래프 출력 (Expected Reach+ 및 Reach3+ 표기)
expected_reach3 = reach_results.get("reach 3+", "N/A")
plot_scatter_with_summary(scatter_data, selected_target, plan_grp, expected_reach_plus, expected_reach3)


# 추가3: X축을 Budget으로 변환하여 그래프 출력

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter  # 정확한 ticker import

def plot_budget_scatter_with_summary(scatter_data, target, plan_grp, expected_reach_plus, expected_reach3, cprp_value):
    """Summary Table 데이터와 동기화된 Budget 기반 Scatter Plot 출력"""
    plt.figure(figsize=(10, 6))

    # Scatter 데이터 중첩 (Budget 변환)
    scatter_target_data = scatter_data[scatter_data['Target'] == target]
    for reach_item in scatter_target_data['reach항목'].unique():
        scatter_subset = scatter_target_data[scatter_target_data['reach항목'] == reach_item]
        budget_values = scatter_subset['GRP'] * (cprp_value / 1000)  # GRP -> Budget 변환
        plt.scatter(
            budget_values, scatter_subset['reach'],
            label=f"Scatter - {reach_item}", alpha=0.7, edgecolor='black'
        )

    # Summary Table 기반 점 추가 (Budget 변환)
    if expected_reach_plus not in ["N/A", 0]:
        budget_for_reach_plus = plan_grp * (cprp_value / 1000)
        plt.scatter([budget_for_reach_plus], [expected_reach_plus], color="red", s=150, label="Expected Reach+", marker="X")

    if expected_reach3 not in ["N/A", 0]:
        budget_for_reach3 = plan_grp * (cprp_value / 1000)
        plt.scatter([budget_for_reach3], [expected_reach3], color="blue", s=150, label="Expected Reach3+", marker="o")

    # X축 라벨을 일반 숫자로 설정 (과학적 표기법 제거)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    plt.title(f"Budget-based Scatter Plot with Summary Data for {target}")
    plt.xlabel("Budget (1,000 KRW)")
    plt.ylabel("Reach (%)")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# 세 번째 그래프 출력
if cprp_value:
    plot_budget_scatter_with_summary(
        scatter_data, 
        selected_target, 
        plan_grp, 
        expected_reach_plus, 
        expected_reach3, 
        cprp_value
    )
