import os
import pandas as pd

# 文件路径
DATA_DIR = "F:\VAS_4.1\data"  # 替换为实际路径
PATIENTS_FILE = os.path.join(DATA_DIR, "PATIENTS.csv")
CHARTEVENTS_FILE = os.path.join(DATA_DIR, "CHARTEVENTS.csv")
D_ITEMS_FILE = os.path.join(DATA_DIR, "D_ITEMS.csv")

# 选择需要的生命体征项目
VITAL_SIGNS = ['PEEP Set', 'PEEP set', 'Heart Rate', 'Peak Insp. Pressure', 'Respiratory Rate', 'FiO2 Set', 'SpO2', 'Spon. Vt (L) (Mech.)', 'Spont Vt', 'Tidal Volume (Obser)', 'Tidal Volume (observed)', 'Minute Volume(Obser)', 'Minute Volume']

def load_data():
    """
    加载所需的 CSV 文件
    """
    try:
        patients = pd.read_csv(PATIENTS_FILE)
        chartevents = pd.read_csv(CHARTEVENTS_FILE)
        d_items = pd.read_csv(D_ITEMS_FILE)
        print("数据加载成功！")
        return patients, chartevents, d_items
    except Exception as e:
        print("数据加载失败:", e)
        return None, None, None

def extract_vital_signs_with_units(patients, chartevents, d_items):
    """
    提取生命体征数据（包括单位），并关联患者信息
    """
    try:
        # 过滤 D_ITEMS 中的生命体征项目
        vital_signs_items = d_items[d_items['label'].isin(VITAL_SIGNS)]

        # 过滤 CHARTEVENTS 中的相关数据
        vital_signs_data = chartevents[chartevents['itemid'].isin(vital_signs_items['itemid'])]

        # 合并患者信息
        merged_data = vital_signs_data.merge(patients, on="subject_id", how="inner")
        merged_data = merged_data.merge(vital_signs_items[['itemid', 'label', 'unitname' ]], on="itemid", how="inner")

        # 选择必要的列
        result = merged_data[[
            'subject_id', 'itemid', 'gender', 'dob', 'dod', 'dod_hosp', 'dod_ssn', 'charttime', 'label', 'valuenum', 'unitname'
        ]]
        print("成功提取生命体征数据（含单位）！")
        return result
    except Exception as e:
        print("数据提取失败:", e)
        return None

if __name__ == "__main__":
    # 加载数据
    patients, chartevents, d_items = load_data()
    if patients is not None and chartevents is not None and d_items is not None:
        # 提取生命体征数据
        vital_signs_data = extract_vital_signs_with_units(patients, chartevents, d_items)
        if vital_signs_data is not None:
            # 保存为 CSV 文件
            output_file = "vital_signs_with_units.csv"
            vital_signs_data.to_csv(output_file, index=False)
            print(f"生命体征数据（含单位）已保存为 {output_file} 文件！")