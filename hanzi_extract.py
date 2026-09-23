import pandas as pd

def extract_chars_from_exact_column(file_path):
    print(f"正在读取文件: {file_path} ...")
    
    try:
        # skiprows=4 的意思是跳过前4行（第1到第4行）
        # 这样 Pandas 就会自动把你的第5行（ID, 汉字, 常用）当作列名
        df = pd.read_excel(file_path, skiprows=4)
    except Exception as e:
        print(f"读取 Excel 失败，请检查文件名或路径: {e}")
        return ""

    # 检查表格中是否成功识别到“汉字”这一列
    if '汉字' not in df.columns:
        print("未找到名为“汉字”的列，请检查 skiprows 设置是否正确。")
        return ""

    char_list = []
    
    # 直接精确遍历“汉字”这一列下的所有单元格
    for cell in df['汉字']:
        if pd.notna(cell):  # 排除空行
            text = str(cell).strip()
            
            # 提取汉字（保险起见依然过滤一下非汉字字符）
            for char in text:
                if '\u4e00' <= char <= '\u9fa5':
                    char_list.append(char)
    
    # 利用字典键的唯一性去重，并保持原本的排序
    unique_chars = list(dict.fromkeys(char_list))
    
    # 将列表里的字拼成一个长字符串
    result_string = "".join(unique_chars)
    
    print(f"提取完成！共提取出 {len(result_string)} 个纯汉字。")
    return result_string

# ----------------- 测试与生成ID列表 -----------------

if __name__ == "__main__":
    # 请将这里的名字改成你实际的文件名，比如 "3500常用字.xls"
    excel_file = "3500.xls" 
    
    # 1. 提取长字符串
    source_chars = extract_chars_from_exact_column(excel_file)
    
    if source_chars:
        # 2. 生成你要抢注的游戏 ID 列表
        target_ids = []
        for char in source_chars:
            target_ids.append(char)       # 添加单字，如: "一"
            target_ids.append(char * 2)   # 添加双字，如: "一一"
            
        print(f"成功生成了 {len(target_ids)} 个待测试的游戏ID！")
        
        # 打印前 20 个看一眼效果
        print(f"前20个测试ID预览: {target_ids[:20]}")
        
        output_filename = "待测试汉字ID列表.txt"
        print(f"正在导出到文件: {output_filename} ...")
        
        try:
            # 使用 utf-8 编码打开/创建文件，防止中文乱码
            with open(output_filename, "w", encoding="utf-8") as f:
                for game_id in target_ids:
                    f.write(game_id + "\n")  # 每个 ID 占一行
                    
            print(f"✅ 导出完成！请在左侧文件资源管理器中查看 '{output_filename}'")
        except Exception as e:
            print(f"❌ 导出失败: {e}")