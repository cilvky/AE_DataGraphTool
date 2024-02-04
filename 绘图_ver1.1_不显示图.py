import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.lines import Line2D

def plot_graph(script_folder, selected_csv, is_THD_version=False):
    # 读取选择的CSV文件，指定所有列的数据类型为字符串
    csv_path = os.path.join(script_folder, selected_csv)
    df = pd.read_csv(csv_path, header=None, dtype=str)

    # 提取X轴数据
    x_values = pd.to_numeric(df.iloc[0, 1:].values, errors='coerce')

    # 提取Y轴数据
    y_values_list = [pd.to_numeric(df.iloc[i, 1:].values, errors='coerce') for i in range(1, len(df))]

    # 创建图表和坐标轴
    fig, ax = plt.subplots(figsize=(17.8, 9.2))

    # 绘制多条曲线，隐藏数据点
    for i, y_values in enumerate(y_values_list):
        color = ''
        linewidth = 1

        if is_THD_version:
            # THD版本的颜色和线宽设置
            if i == 0:
                color = '#000000'
                linewidth = 3
            elif i % 2 == 1:
                color = '#FF0000'
            else:
                color = '#66FF33'
        else:
            # FR版本的颜色和线宽设置
            if i == 0 or i == 1:
                color = '#000000'
                linewidth = 3
            elif i % 2 == 0:
                color = '#66FF33'
            else:
                color = '#FF0000'

        ax.plot(x_values, y_values, marker='', linestyle='-', linewidth=linewidth, color=color)

    # 设置X轴刻度为对数
    ax.set_xscale('log')

    # 设置X轴刻度为[20, 100, 1000, 10000, 20000]的比例
    desired_xticks = [20, 100, 1000, 10000, 20000]
    ax.set_xticks(desired_xticks)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    # 设置Y轴刻度为对数（仅THD版本）
    if is_THD_version:
        ax.set_yscale('log')
        ax.set_ylim(0.01, 100)  # 固定y轴范围为0.01~100
    else:
        #（FR版本）设置y轴显示范围
        y_axis_range_input = input("请输入y轴显示范围，例如：（85,125），按回车则默认值: ")

        if y_axis_range_input:
            y_axis_range = [float(val.strip()) for val in y_axis_range_input.split(',')]
        else:
            y_axis_range = [max(max(y) for y in y_values_list), min(min(y) for y in y_values_list)]

        ax.set_ylim(min(y_axis_range), max(y_axis_range))  # 保证y轴方向正确

    # 显示主要刻度点的轴线
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # 获取文件名（去除后缀）
    file_name_without_extension = os.path.splitext(selected_csv)[0]

    # 定义需要显示的曲线的 Line2D 对象
    limit_line = Line2D([0], [0], marker='', linestyle='-', linewidth=3, color='#000000', label='Limit')
    left_line = Line2D([0], [0], marker='', linestyle='-', linewidth=1, color='#66FF33', label='Left')
    right_line = Line2D([0], [0], marker='', linestyle='-', linewidth=1, color='#FF0000', label='Right')

    # 显示图例，设置字体大小为16，指定 handles 和 labels
    plt.legend(handles=[limit_line, left_line, right_line], loc='lower left', fontsize=14)

    # 设置图表标题和标签
    ax.set_title(file_name_without_extension, fontsize=26, pad=16)  
    ax.set_xlabel(f'Frequency [Hz]', fontsize=18, labelpad=8)  
    ax.set_ylabel('SPL [dB]' if not is_THD_version else 'Ratio[%]', fontsize=18, labelpad=10)  

    # 设置X轴刻度为[20, 100, 1000, 10000, 20000]的比例（FR版本）
    if not is_THD_version:
        ax.set_xticks(desired_xticks)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    # 设置Y轴刻度为[0.01, 0.1, 1, 10, 100]（仅THD版本）
    if is_THD_version:
        desired_yticks = [0.01, 0.1, 1, 10, 100]
        ax.set_yticks(desired_yticks)
        ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())

    # 设置轴线刻度点的字体大小
    ax.tick_params(axis='both', labelsize=15)  

    # 显示组数目
    num_of_groups = len(y_values_list)
    ax.text(0.995, 0.99, f'Number of curves: {num_of_groups}', ha='right', va='top', transform=ax.transAxes, fontsize=15)

    # 显示数量信息
    Number_of_units = int((num_of_groups - 2) / 2) if not is_THD_version else int((num_of_groups - 1) / 2)
    ax.text(0.995, 0.95, f'Units: {Number_of_units}', ha='right', va='top', transform=ax.transAxes, fontsize=15)

    # 保存图片在当前脚本文件夹内
    output_file_path = os.path.join(script_folder, f'{file_name_without_extension}_output.png')

    # 以180dpi分辨率保存图表，并调整图形显示边距
    plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.1)
    plt.savefig(output_file_path, dpi=180)

    # 打印保存的文件路径
    print(f"图表已保存至：{output_file_path}")
    print("完成！")
    
    # 显示图表
    #plt.show()


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
