import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.lines import Line2D

def plot_graph(script_folder, selected_csv, is_THD_version=False):
    # 读取CSV文件
    csv_path = os.path.join(script_folder, selected_csv)
    df = pd.read_csv(csv_path, header=None, dtype=str)

    # 提取X轴数据
    x_values = pd.to_numeric(df.iloc[0, 1:].values, errors='coerce')

    # 提取Y轴数据列表
    y_values_list = [pd.to_numeric(df.iloc[i, 1:].values, errors='coerce') for i in range(1, len(df))]

    # 创建图表和坐标轴
    fig, ax = plt.subplots(figsize=(17.8, 9.2))
    color_sources_dict = {}

    # 遍历Y轴数据，绘制曲线
    for i, y_values in enumerate(y_values_list):
        line_info = df.iloc[i + 1, 0]
        color, linewidth = get_color_and_linewidth(line_info)

        # 记录颜色对应的数据源
        color_sources_dict.setdefault(color, []).append(line_info)

        # 提取图例显示的标签
        legend_label = line_info.split('-')[0]

        # 绘制曲线
        ax.plot(x_values, y_values, marker='', linestyle='-', linewidth=linewidth, color=color, label=legend_label)

    # 生成图例内容
    legend_handles = []
    for color, sources in color_sources_dict.items():
        # 对于每个颜色，创建一个Line2D对象
        line_info = sources[0]
        label ='Limit' if 'limit' in line_info.lower() else line_info.split('-')[0] # 如果包含"limit"，则名字为 Limit
        linewidth = 3 if 'limit' in line_info.lower() else 1  # 如果包含"limit"，则线宽为3，否则为1
        legend_line = Line2D([0], [0], marker='', linestyle='-', linewidth=linewidth, color=color, label=label)
        legend_handles.append(legend_line)
        
    # 显示图例
    plt.legend(handles=legend_handles, loc='lower left', fontsize=14)

    # 设置X轴为对数刻度
    ax.set_xscale('log')
    ax.set_xticks([20, 100, 1000, 10000, 20000])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    # 设置Y轴刻度范围和刻度值（THD版本和FR版本分别处理）
    if is_THD_version:
        ax.set_yscale('log')
        ax.set_ylim(0.01, 100)  # 固定y轴范围为0.01~100
    else:
        y_axis_range = get_y_axis_range(y_values_list)

        # 获取Y轴范围输入（仅FR版本）
        y_axis_range_input = input("请输入y轴显示范围，例如：（85,125），按回车则默认值: ")

        if y_axis_range_input:
            y_axis_range = [float(val.strip()) for val in y_axis_range_input.split(',')]
        else:
            y_axis_range = [max(max(y) for y in y_values_list), min(min(y) for y in y_values_list)]

        ax.set_ylim(min(y_axis_range), max(y_axis_range))  # 保证y轴方向正确

    # 显示主要刻度点的网格线
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # 获取文件名（去除后缀）
    file_name_without_extension = os.path.splitext(selected_csv)[0]

    # 设置图表标题和标签
    ax.set_title(file_name_without_extension, fontsize=26, pad=16)
    ax.set_xlabel(f'Frequency [Hz]', fontsize=18, labelpad=8)
    ax.set_ylabel('SPL [dB]' if not is_THD_version else 'Ratio[%]', fontsize=18, labelpad=10)

    # 针对FR版本设置X轴刻度
    if not is_THD_version:
        ax.set_xticks([20, 100, 1000, 10000, 20000])
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    # 针对THD版本设置Y轴刻度
    if is_THD_version:
        ax.set_yticks([0.01, 0.1, 1, 10, 100])
        ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())

    # 设置轴线刻度点的字体大小
    ax.tick_params(axis='both', labelsize=15)

    # 显示曲线数目
    num_of_groups = len(y_values_list)
    ax.text(0.995, 0.99, f'Number of curves: {num_of_groups}', ha='right', va='top', transform=ax.transAxes, fontsize=15)

    # 保存图片在当前脚本文件夹内
    output_file_path = os.path.join(script_folder, f'{file_name_without_extension}_output.png')

    # 以180dpi分辨率保存图表，并调整图形显示边距
    plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.1)
    plt.savefig(output_file_path, dpi=180)

    # 打印保存的文件路径
    print(f"图表已保存至：{output_file_path}")
    print("完成！")

def get_color_and_linewidth(line_info):
    # 定义颜色映射关系
    color_mapping = {'#A': '#66FF33', '#B': '#FF0000', '#C': '#00B0F0', '#D': '#FFC000', '#E': '#808000',
                     '#F': '#7030A0', '#G': '#00ffff', '#H': '#FF00FF'}
    default_color, default_linewidth = '#000000', 1

    # 判断是否为特殊线条（limit）或普通线条，选择颜色和线宽
    if 'limit' in line_info.lower():
        return default_color, 3
    else:
        for key, value in color_mapping.items():
            if key in line_info:
                return value, default_linewidth

    return None, None

def get_y_axis_range(y_values_list):
    # 获取Y轴范围，保证能够正确显示曲线
    y_min = min(min(y) for y in y_values_list)
    y_max = max(max(y) for y in y_values_list)
    return [y_max, y_min]

if __name__ == "__main__":
    # 获取当前脚本所在的文件夹路径
    script_folder = os.path.dirname(os.path.abspath(__file__))

    # 列出文件夹内所有CSV文件
    csv_files = [file for file in os.listdir(script_folder) if file.endswith('.csv')]

    # 打印文件列表并让用户选择
    print("请选择功能:")
    print("1. 绘制FR曲线图")
    print("2. 绘制THD曲线图")

    try:
        user_choice = int(input("请输入选择的数字: "))
        selected_csv = None

        if user_choice == 1 or user_choice == 2:
            print("请选择数据源:")
            for i, csv_file in enumerate(csv_files):
                print(f"{i+1}. {csv_file}")
            selected_csv = csv_files[int(input("请输入选择的数字: ")) - 1]

            plot_graph(script_folder, selected_csv, is_THD_version=(user_choice == 2))
        else:
            print("无效的选择。")

    except ValueError:
        print("输入无效。")
