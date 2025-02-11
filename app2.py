import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

import collections.abc #에러가나면, 한줄 띄거나 붙이거나 해서 새로고침하기


# 1. 하드코딩 데이터 삽입
def insert_hardcoded_data():
    data = {
        "target": [
            "40세이상", "40세이상", "40세이상", "40세이상", "40세이상", "40세이상", "40세이상", "40세이상", "40세이상", "40세이상", "40세이상",
            "20세이상", "20세이상", "20세이상", "20세이상", "20세이상", "20세이상", "20세이상", "20세이상", "20세이상", "20세이상", "20세이상",
            "대학생", "대학생", "대학생", "대학생", "대학생", "대학생", "대학생", "대학생", "대학생", "대학생", "대학생",
            "중/고등학생", "중/고등학생", "중/고등학생", "중/고등학생", "중/고등학생", "중/고등학생", "중/고등학생", "중/고등학생", "중/고등학생", "중/고등학생", "중/고등학생",
            "3049P", "3049P", "3049P", "3049P", "3049P", "3049P", "3049P", "3049P", "3049P", "3049P", "3049P",
            "3559P", "3559P", "3559P", "3559P", "3559P", "3559P", "3559P", "3559P", "3559P", "3559P", "3559P",
            "2544F", "2544F", "2544F", "2544F", "2544F", "2544F", "2544F", "2544F", "2544F", "2544F", "2544F",
            "2549F", "2549F", "2549F", "2549F", "2549F", "2549F", "2549F", "2549F", "2549F", "2549F", "2549F",
            "1019P", "1019P", "1019P", "1019P", "1019P", "1019P", "1019P", "1019P", "1019P", "1019P", "1019P",
            "2029P", "2029P", "2029P", "2029P", "2029P", "2029P", "2029P", "2029P", "2029P", "2029P", "2029P",
            "3039P", "3039P", "3039P", "3039P", "3039P", "3039P", "3039P", "3039P", "3039P", "3039P", "3039P",
            "4049P", "4049P", "4049P", "4049P", "4049P", "4049P", "4049P", "4049P", "4049P", "4049P", "4049P",
            "5059P", "5059P", "5059P", "5059P", "5059P", "5059P", "5059P", "5059P", "5059P", "5059P", "5059P",
            "1019M", "1019M", "1019M", "1019M", "1019M", "1019M", "1019M", "1019M", "1019M", "1019M", "1019M",
            "2029M", "2029M", "2029M", "2029M", "2029M", "2029M", "2029M", "2029M", "2029M", "2029M", "2029M",
            "3039M", "3039M", "3039M", "3039M", "3039M", "3039M", "3039M", "3039M", "3039M", "3039M", "3039M",
            "4049M", "4049M", "4049M", "4049M", "4049M", "4049M", "4049M", "4049M", "4049M", "4049M", "4049M",
            "5059M", "5059M", "5059M", "5059M", "5059M", "5059M", "5059M", "5059M", "5059M", "5059M", "5059M",
            "1019F", "1019F", "1019F", "1019F", "1019F", "1019F", "1019F", "1019F", "1019F", "1019F", "1019F",
            "2029F", "2029F", "2029F", "2029F", "2029F", "2029F", "2029F", "2029F", "2029F", "2029F", "2029F",
            "3039F", "3039F", "3039F", "3039F", "3039F", "3039F", "3039F", "3039F", "3039F", "3039F", "3039F",
            "4049F", "4049F", "4049F", "4049F", "4049F", "4049F", "4049F", "4049F", "4049F", "4049F", "4049F",
            "5059F", "5059F", "5059F", "5059F", "5059F", "5059F", "5059F", "5059F", "5059F", "5059F", "5059F",
            "2034F", "2034F", "2034F", "2034F", "2034F", "2034F", "2034F", "2034F", "2034F", "2034F", "2034F",
            "1834F", "1834F", "1834F", "1834F", "1834F", "1834F", "1834F", "1834F", "1834F", "1834F", "1834F",
        ],
        "channel": [
            "TV", "VA", "DA", "TV∪VA", "VA∪DA", "TV∪DA", "TV∪DA∪VA", "TV∩VA", "TV∩DA", "VA∩DA", "TV∩DA∩VA"
        ] * 23,  # 각 타겟마다 11개의 채널이 동일하게 반복
        "reach": [
            59, 47.5, 61.2, 77.5, 68.9, 83, 87.1, 29, 37.2, 39.8, 25.4,
            48.8, 49.9, 62.7, 77.7, 70.2, 84.6, 90, 21, 26.9, 42.4, 18.9,
            38.9, 49.6, 64.1, 75.2, 70, 86.8, 91.6, 13.3, 16.2, 43.7, 12.2,
            29.7, 66.2, 67.6, 83.6, 76.7, 85, 92.7, 12.3, 12.3, 57.1, 10.9,
            49.9, 50.6, 64.4, 71.1, 72, 85.6, 83.8, 29.4, 28.7, 43, 20,
            56.3, 49.1, 62.3, 78, 70, 83.6, 88, 27.4, 35, 41.4, 24.1,
            47.3, 51.2, 65.6, 77.7, 72.7, 86.3, 91.5, 20.8, 26.6, 44.1, 18.9,
            47.6, 50.5, 63, 77.5, 70.5, 84.6, 89.9, 20.6, 26, 43, 18.4,
            30.3,63.1,61.3,81,74.4,84.3,91.6,12.4,7.3,50,6.6,
            38.9,50.5,61.5,75.8,68.2,83.8,89.8,13.6,16.6,43.8,12.9,
            43.5,53.1,66.3,79.9,74.5,88.1,94.6,16.7,21.7,44.9,15,
            56.4,48.2,62.5,76,69.6,83.4,86.8,28.6,35.5,41.1,24.9,
            64.1,46,58.3,80.4,67.4,82.2,87.7,29.7,40.2,36.9,26.1,
            22.6,59.9,65,72.2,71.5,75.9,81.7,10.3,11.7,53.4,9.6,
            36.4,45.8,59.6,73.5,66.6,84.4,89.8,8.7,11.6,38.8,7.1,
            40.7,54.9,64.7,79.6,73.4,85.5,92.3,16,19.9,46.2,14.1,
            55.3,48.7,64.3,76.8,71.6,83.7,87.7,27.2,35.9,41.4,23.9,
            63,42,57.2,78.2,65.2,82.5,87.6,26.8,37.7,34,23.9,
            38,66.4,69.4,89.8,79.5,92.7,101.5,14.6,14.7,56.3,13.3,
            41.1,55.3,63.3,77.8,69.8,82.9,89,18.6,21.5,48.8,18.2,
            46.2,56.4,68,81.5,75.7,90.6,96.8,21.1,23.6,48.7,19.6,
            57.5,47.6,60.8,75.3,67.6,82.9,85.8,29.8,35.4,40.8,25.9,
            65.2,50,59.4,82.6,69.6,81.9,87.6,32.6,42.7,39.8,28.1,
            40.3,55,65.4,79.6,73,86,93.1,15.7,19.7,47.4,15.2,
            40.1,55.4,65.8,80.4,73.1,87.4,94.3,15.1,18.5,48.1,14.7,
        ]
    }
    # target 개수 확인
    num_targets = len(data["target"])

    # channel 리스트 길이 조정
    channel_list = ["TV", "VA", "DA", "TV∪VA", "VA∪DA", "TV∪DA", "TV∪DA∪VA", "TV∩VA", "TV∩DA", "VA∩DA", "TV∩DA∩VA"]
    data["channel"] = (channel_list * (num_targets // len(channel_list) + 1))[:num_targets]

    # reach 리스트 길이 조정
    reach_values = [59, 47.5, 61.2, ..., 14.7]  # 기존 reach 값
    data["reach"] = (reach_values * (num_targets // len(reach_values) + 1))[:num_targets]

    # 길이 출력 (디버깅용)
    print(f"target 개수: {len(data['target'])}")
    print(f"channel 개수: {len(data['channel'])}")
    print(f"reach 개수: {len(data['reach'])}")

    return pd.DataFrame(data)

# 2. 데이터 로드
def load_data():
    data = insert_hardcoded_data()
    available_targets = data["target"].unique()
    selected_target = st.selectbox("타겟을 선택하세요:", available_targets)
    filtered_data = data[data["target"] == selected_target]
    return filtered_data, selected_target

# Streamlit 도달률 계산
def calculate_reach(tv_reach, va_reach, da_reach, filtered_data, stats_population, tv_population, digital_population):
    original_reach = filtered_data.set_index("channel")["reach"].to_dict()

    # 교차 도달률 비율 계산
    ratios = {
        'TV∩VA': original_reach.get('TV∩VA', 0) / original_reach.get('TV', 1),
        'TV∩DA': original_reach.get('TV∩DA', 0) / original_reach.get('TV', 1),
        'VA∩DA': original_reach.get('VA∩DA', 0) / original_reach.get('VA', 1),
        'TV∩DA∩VA': original_reach.get('TV∩DA∩VA', 0) / original_reach.get('TV∪DA∪VA', 1)
    }

    # 교차 도달률 가중치 설정
    weight_factors = {
        'TV∩VA': 1,
        'TV∩DA': 1,
        'VA∩DA': 0.742,
        'TV∩DA∩VA': 1
    }

    # Reach Values 계산
    reach_values = {
        'TV': tv_reach,
        'VA': va_reach,
        'DA': da_reach,
        'TV∪VA': tv_reach + va_reach - (min(tv_reach, va_reach) * ratios['TV∩VA'] * weight_factors['TV∩VA']),
        'VA∪DA': va_reach + da_reach - (min(va_reach, da_reach) * ratios['VA∩DA'] * weight_factors['VA∩DA']),
        'TV∪DA': tv_reach + da_reach - (min(tv_reach, da_reach) * ratios['TV∩DA'] * weight_factors['TV∩DA']),
        'TV∪DA∪VA': tv_reach + va_reach + da_reach
                     - (min(tv_reach, va_reach) * ratios['TV∩VA'] * weight_factors['TV∩VA'])
                     - (min(tv_reach, da_reach) * ratios['TV∩DA'] * weight_factors['TV∩DA'])
                     - (min(va_reach, da_reach) * ratios['VA∩DA'] * weight_factors['VA∩DA'])
                     + (min(tv_reach, va_reach, da_reach) * ratios['TV∩DA∩VA'] * weight_factors['TV∩DA∩VA']),
        'TV∩VA': min(tv_reach, va_reach) * ratios['TV∩VA'] * weight_factors['TV∩VA'],
        'TV∩DA': min(tv_reach, da_reach) * ratios['TV∩DA'] * weight_factors['TV∩DA'],
        'VA∩DA': min(va_reach, da_reach) * ratios['VA∩DA'] * weight_factors['VA∩DA'],
        'TV∩DA∩VA': min(tv_reach, va_reach, da_reach) * ratios['TV∩DA∩VA'] * weight_factors['TV∩DA∩VA']
    }

    # Pure Reach Values 계산 및 음수 처리
    pure_reach_values = {
        'Pure TV': max(0, reach_values['TV'] - reach_values['TV∩VA'] - reach_values['TV∩DA'] + reach_values['TV∩DA∩VA']),
        'Pure VA': max(0, reach_values['VA'] - reach_values['TV∩VA'] - reach_values['VA∩DA'] + reach_values['TV∩DA∩VA']),
        'Pure DA': max(0, reach_values['DA'] - reach_values['TV∩DA'] - reach_values['VA∩DA'] + reach_values['TV∩DA∩VA'])
    }

    # Pure Reach Values 반영
    reach_values.update(pure_reach_values)

    # 도달률 상한선 적용
    for key in reach_values:
        reach_values[key] = min(100, max(0, reach_values[key]))

    # Reach Population 계산
    reach_population = {
        'TV': 0.01 * (reach_values['TV'] * tv_population),
        'VA': 0.01 * (reach_values['VA'] * digital_population),
        'DA': 0.01 * (reach_values['DA'] * digital_population),
        'TV∪VA': 0.01 * ((reach_values['TV'] * tv_population) + (reach_values['VA'] * digital_population) - (reach_values['TV∩VA'] * tv_population)),
        'TV∪DA': 0.01 * ((reach_values['TV'] * tv_population) + (reach_values['DA'] * digital_population) - (reach_values['TV∩DA'] * tv_population)),
        'VA∪DA': 0.01 * ((reach_values['VA'] * digital_population) + (reach_values['DA'] * digital_population) - (reach_values['VA∩DA'] * digital_population)),
        'TV∪DA∪VA': 0.01 * ((reach_values['TV'] * tv_population) + (reach_values['VA'] * digital_population) + (reach_values['DA'] * digital_population) - 
                            (reach_values['VA∩DA'] * digital_population) - (reach_values['TV∩DA'] * tv_population) - 
                            (reach_values['TV∩VA'] * tv_population) + (reach_values['TV∩DA∩VA'] * tv_population)),
        'TV∩VA': 0.01 * (reach_values['TV∩VA'] * tv_population),
        'TV∩DA': 0.01 * (reach_values['TV∩DA'] * tv_population),
        'VA∩DA': 0.01 * (reach_values['VA∩DA'] * digital_population),
        'TV∩DA∩VA': 0.01 * (reach_values['TV∩DA∩VA'] * tv_population),
        'Pure TV': 0.01 * (reach_values['Pure TV'] * tv_population),
        'Pure VA': 0.01 * (reach_values['Pure VA'] * digital_population),
        'Pure DA': 0.01 * (reach_values['Pure DA'] * digital_population)
    }

    # Reach Stats 계산
    reach_stats = {
        key: (value / stats_population) * 100 for key, value in reach_population.items()
    }

    # DataFrame 생성
    result_df = pd.DataFrame({
        "Metric": reach_values.keys(),
        "Reach (%)": reach_values.values(),
        "Population (명)": [f"{int(val):,}" for val in reach_population.values()],
        "Reach Stats (%)": [f"{round(val, 2):,.2f}%" for val in reach_stats.values()]
    })

    return result_df


# 4. Venn Diagram
def plot_venn_diagram(reach_stats):
    try:
        # reach_stats 값이 문자열인지 확인 후, float으로 변환
        reach_stats = {
            key: float(value.replace('%', '')) if isinstance(value, str) and '%' in value else value
            for key, value in reach_stats.items()
        }

        # Venn 다이어그램의 각 영역에 출력할 값 설정
        subsets = (
            reach_stats.get('TV', 0),
            reach_stats.get('VA', 0),
            reach_stats.get('DA', 0),
            reach_stats.get('TV∩VA', 0),
            reach_stats.get('TV∩DA', 0),
            reach_stats.get('VA∩DA', 0),
            reach_stats.get('TV∩DA∩VA', 0)
        )

        # Venn 다이어그램 생성
        plt.figure(figsize=(8, 8))
        venn = venn3(subsets=subsets, set_labels=('TV', 'VA(digital video)', 'DA(digital display ad)'))

        # 각 영역에 도달률 표시
        if venn.get_label_by_id('100'):
            venn.get_label_by_id('100').set_text(f"{subsets[0]:.1f}%")
        if venn.get_label_by_id('010'):
            venn.get_label_by_id('010').set_text(f"{subsets[1]:.1f}%")
        if venn.get_label_by_id('001'):
            venn.get_label_by_id('001').set_text(f"{subsets[2]:.1f}%")
        if venn.get_label_by_id('110'):
            venn.get_label_by_id('110').set_text(f"{subsets[3]:.1f}%")
        if venn.get_label_by_id('101'):
            venn.get_label_by_id('101').set_text(f"{subsets[4]:.1f}%")
        if venn.get_label_by_id('011'):
            venn.get_label_by_id('011').set_text(f"{subsets[5]:.1f}%")
        if venn.get_label_by_id('111'):
            venn.get_label_by_id('111').set_text(f"{subsets[6]:.1f}%")

        # 다이어그램 제목 설정
        plt.title("Reach Stats Venn Diagram")
        st.pyplot(plt)  # Streamlit에 플롯 표시
    except Exception as e:
        st.error(f"Error in plotting Venn Diagram: {e}")

# 5. TV∪DA∪VA 도달률 및 도달 인구 출력
def print_final_reach_percentage(result_df, stats_population, tv_population, digital_population):
    try:
        # TV∪DA∪VA 도달률 및 인구 계산
        tv_reach = result_df.loc[result_df["Metric"] == "TV", "Reach (%)"].iloc[0]
        va_reach = result_df.loc[result_df["Metric"] == "VA", "Reach (%)"].iloc[0]
        da_reach = result_df.loc[result_df["Metric"] == "DA", "Reach (%)"].iloc[0]
        tv_va_reach = result_df.loc[result_df["Metric"] == "TV∩VA", "Reach (%)"].iloc[0]
        tv_da_reach = result_df.loc[result_df["Metric"] == "TV∩DA", "Reach (%)"].iloc[0]
        va_da_reach = result_df.loc[result_df["Metric"] == "VA∩DA", "Reach (%)"].iloc[0]
        tv_da_va_reach = result_df.loc[result_df["Metric"] == "TV∩DA∩VA", "Reach (%)"].iloc[0]

        # 도달 인구 계산
        reach_population = (
            tv_population * tv_reach * 0.01
            + digital_population * da_reach * 0.01
            + digital_population * va_reach * 0.01
            - tv_population * tv_va_reach * 0.01
            - tv_population * tv_da_reach * 0.01
            - digital_population * va_da_reach * 0.01
            + tv_population * tv_da_va_reach * 0.01
        )

        # 도달률 계산
        reach_percentage = (reach_population / stats_population) * 100

        # Streamlit으로 결과 출력
        st.subheader("TV∪DA∪VA 통합도달률 및 통합도달 인구") 
        st.markdown(f"- **통합도달률 (Reach Rate)**: {reach_percentage:.2f}%")
        st.markdown(f"- **통합도달 인구 (Reach Population)**: {reach_population:,.0f}명")

    except Exception as e:
        st.error(f"Error in calculating final reach percentage: {e}")

# 메인
def main():
    st.title("Total Reach Analysis Application(TV&Digital Video/DA)") 
    st.write("타겟 데이터를 선택하고 입력값을 기반으로 통합도달률을 계산하세요.") 

    # 데이터 로드
    filtered_data, selected_target = load_data()
    st.write(f"선택된 타겟: {selected_target}")
    st.dataframe(filtered_data)

    # 사용자 입력
    st.subheader("모집단 정보 입력")
    stats_population = st.number_input("Statistics Korea Population (명)", min_value=0, value=1000000, step=1000)
    tv_population = st.number_input("TV Population (명)", min_value=0, value=500000, step=1000)
    digital_population = st.number_input("Digital Population (명)", min_value=0, value=500000, step=1000)

    st.subheader("도달률 입력")
    tv_reach = st.number_input("TV 도달률 (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    va_reach = st.number_input("VA 도달률 (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    da_reach = st.number_input("DA 도달률 (%)", min_value=0.0, max_value=100.0, step=0.1)

    # 계산 수행
    result_df = calculate_reach(tv_reach, va_reach, da_reach, filtered_data, stats_population, tv_population, digital_population)

    # 결과 출력
    st.subheader("도달률 계산 결과")
    st.dataframe(result_df)

    # Venn Diagram 출력
    st.subheader("Venn Diagram")
    plot_venn_diagram(result_df.set_index("Metric")["Reach Stats (%)"].to_dict())

    # TV∪DA∪VA 도달률 및 도달 인구 출력
    print_final_reach_percentage(result_df, stats_population, tv_population, digital_population)

if __name__ == "__main__":
    main()
