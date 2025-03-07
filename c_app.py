import streamlit as st
import psycopg2
import os
import json  # 導入 json 函式庫

from nosync import db_setting

class DatabaseConnector:
    """處理資料庫連線"""
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = self._init_connection()

    def _init_connection(self):
        """初始化資料庫連線"""
        try:
            conn = psycopg2.connect(self.db_url)
            return conn
        except Exception as e:
            st.error(f"資料庫連線錯誤：{e}")
            return None

    def get_connection(self):
        """取得資料庫連線物件"""
        return self.conn

class FlavorDataHandler:
    """處理風味資料"""
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.flavor_categories, self.flavor_details = self._load_flavor_data()

    def _load_flavor_data(self):
        """從 JSON 檔案載入風味資料"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:  # 指定編碼為 utf-8
                flavor_data = json.load(f)
                flavor_categories = flavor_data['flavor_categories']  # 從 JSON 資料中讀取 flavor_categories
                flavor_details = flavor_data['flavor_details']  # 從 JSON 資料中讀取 flavor_details
                return flavor_categories, flavor_details
        except FileNotFoundError:
            st.error(f"找不到 {self.json_file_path} 檔案，請確認檔案是否存在於程式碼目錄下。")
            return {}, {}
        except json.JSONDecodeError:
            st.error(f"{self.json_file_path} 檔案格式錯誤，請檢查 JSON 檔案內容是否正確。")
            return {}, {}

class RecordForm:
    """處理新增紀錄表單頁面"""
    def __init__(self, db_connector, flavor_handler):
        self.db_connector = db_connector
        self.flavor_handler = flavor_handler
        self.conn = self.db_connector.get_connection() # 取得資料庫連線
        self.flavor_categories = self.flavor_handler.flavor_categories
        self.flavor_details = self.flavor_handler.flavor_details

    def show_add_record_page(self):
        """顯示新增紀錄頁面"""
        st.title('新增咖啡品嚐紀錄')
        st.write('在這裡新增您的咖啡品嚐筆記！')

        # --- 初始化 coffee_brand 變數 ---
        coffee_brand = None  # 或者 coffee_brand = ""
        # --- 初始化變數結束 ---

        # --- 新增紀錄項目 ---
        record_date = st.date_input("品嚐日期")  # 日期輸入

        # 品牌下拉式選單 (選項包含 "新增品牌...")
        brand_options = self._get_brand_options_from_db()
        brand_options_with_new = ["新增品牌..."] + brand_options  # 在選項列表最前面加入 "新增品牌..."
        selected_brand_option = st.selectbox("咖啡品牌", options=brand_options_with_new, index=0)

        new_brand_input = None  # 初始化 new_brand_input 變數

        if selected_brand_option == "新增品牌...":  # 如果使用者選擇了 "新增品牌..." 選項
            new_brand_input = st.text_input("請輸入新的咖啡品牌")  # 顯示文字輸入框，讓使用者輸入新的品牌

        # 在提交紀錄時，判斷使用者是選擇了下拉選單的品牌，還是輸入了新的品牌
        if st.button('新增品牌'):
            if new_brand_input:  # 如果 new_brand_input 有值，表示使用者輸入了新的品牌
                coffee_brand = new_brand_input  # 移除 coffee_brand = 定義，只保留賦值
            else:  # 否則，使用 selectbox 選擇的品牌
                coffee_brand = selected_brand_option  # 移除 coffee_brand = 定義，只保留賦值
        st.write(f"您選擇的咖啡品牌是：{coffee_brand}")  # <= coffee_brand is working


        # 產地下拉式選單 + 自動完成 (保持 selectbox)
        origin_options = self._get_origin_options_from_db()
        coffee_origin = st.selectbox("咖啡產地", options=[""] + origin_options, index=0)  # 產地下拉選單，選項包含歷史產地，預設為空
        # --- 新增紀錄項目結束 ---

        coffee_name = st.text_input('咖啡名稱')
        # 將烘焙程度改為滑桿 (範圍 1-10)
        roast_level = st.slider('烘焙程度 (1-10)', 1, 10, 5)  # 預設值設為 5
        # 增加酸度滑桿 (範圍 1-10)
        acidity_level = st.slider('酸度 (1-10)', 1, 10, 5)  # 預設值設為 5
        # 增加苦度滑桿 (範圍 1-10)
        bitterness_level = st.slider('苦度 (1-10)', 1, 10, 5)  # 預設值設為 5

        feedback = st.feedback(
            options="stars",
            key="coffee_rating_feedback",
        )  # 為 feedback 元件設定一個唯一的 key

        st.header('選擇咖啡風味 (三層選單)')

        primary_category_options = list(self.flavor_categories.keys())
        selected_primary_category = st.multiselect("主要風味類別 (第一層)", primary_category_options)

        subcategory_options = []
        if selected_primary_category:
            for category in selected_primary_category:  # Iterate through selected primary categories
                subcategory_options.extend(self.flavor_categories[category])  # Add subcategories from each selected category
        selected_subcategory = st.multiselect("次要風味類別 (第二層)", subcategory_options)

        detail_flavor_options = []
        if selected_subcategory:
            for subcategory in selected_subcategory:  # Iterate through selected subcategories
                if subcategory in self.flavor_details:  # Check if subcategory has details in flavor_details dictionary
                    detail_flavor_options.extend(self.flavor_details[subcategory])  # Add details for each selected subcategory
        selected_detail_flavor = st.multiselect("詳細風味 (第三層)", detail_flavor_options)

        taste_notes = st.text_area('品嚐筆記')

        # Combine all selected flavors from all levels into a single list
        all_selected_flavors = []
        if selected_primary_category:
            all_selected_flavors.extend(selected_primary_category)
        if selected_subcategory:
            all_selected_flavors.extend(selected_subcategory)
        if selected_detail_flavor:
            all_selected_flavors.extend(selected_detail_flavor)
        st.session_state.selected_flavors = all_selected_flavors  # Update session state with combined selections

        # Display currently selected flavors
        if st.button('顯示紀錄'):
            st.write('---')
            st.write('**品嚐日期:**', record_date)  # 顯示日期
            st.write('**咖啡品牌:**', coffee_brand)  # 顯示品牌 - 使用 selectbox 的值 ===> coffee_brand is not working
            st.write('**咖啡產地:**', coffee_origin)  # 顯示產地
            st.write('**咖啡名稱:**', coffee_name)
            # 顯示滑桿數值
            st.write('**烘焙程度:**', roast_level)
            st.write('**酸度:**', acidity_level)
            st.write('**苦度:**', bitterness_level)
            st.write('**品嚐筆記:**', taste_notes)
            st.write('**咖啡風味:**', st.session_state.selected_flavors)
            if feedback:  # 檢查 feedback 物件和評分值是否存在
                st.write('**咖啡評分:**', "⭐" * feedback)  # 顯示 feedback 中的星級評分 (星星符號)
            else:
                st.write('**咖啡評分:** 尚未評分')  # 如果沒有評分，顯示 "尚未評分"
            st.write('---')
            st.write('紀錄已新增！ (目前僅為顯示，尚未儲存)')

        if st.button('提交紀錄'):
            if st.session_state.selected_flavors:
                if self.conn:  # 檢查資料庫連線是否建立成功
                    try:
                        cursor = self.conn.cursor()
                        # 建立資料表欄位 (如果不存在) - 只需執行一次 (為了新增 date, brand, origin 欄位)
                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS coffee_records (
                                id SERIAL PRIMARY KEY,
                                record_date DATE,          -- 品嚐日期 (DATE 類型)
                                coffee_brand VARCHAR(255),   -- 咖啡品牌
                                coffee_origin VARCHAR(255),  -- 咖啡產地
                                coffee_name VARCHAR(255),
                                roast_level VARCHAR(50),  -- 烘焙程度改為數值，但資料庫欄位型態先保持 VARCHAR
                                acidity_level INTEGER,     -- 酸度欄位 (整數)
                                bitterness_level INTEGER,  -- 苦度欄位 (整數)
                                taste_notes TEXT,
                                coffee_flavors VARCHAR(255),
                                coffee_rating INTEGER
                            );
                        """)
                        self.conn.commit()  # 提交資料表結構變更

                        # 將風味列表轉換為逗號分隔的字串
                        flavor_string = ", ".join(st.session_state.selected_flavors)
                        rating_value = feedback if feedback else None  # 取得評分值，沒有評分則為 None

                        # 插入資料到資料庫 (包含 date, brand, origin 欄位)
                        cursor.execute("""
                            INSERT INTO coffee_records (record_date, coffee_brand, coffee_origin, coffee_name, roast_level, acidity_level, bitterness_level, taste_notes, coffee_flavors, coffee_rating)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """, (record_date, coffee_brand, coffee_origin, coffee_name, str(roast_level), acidity_level, bitterness_level, taste_notes, flavor_string, rating_value))  # roast_level 轉為字串儲存
                        self.conn.commit()  # 提交資料插入

                        st.success('品嚐紀錄已提交並儲存到 Neon 資料庫！')
                        st.session_state.coffee_records = []  # 清空 session_state 中的紀錄
                        st.session_state.selected_flavors = []
                    except Exception as e:
                        st.error(f"提交紀錄到資料庫時發生錯誤：{e}")
                else:
                    st.error("無法連線到資料庫，請檢查連線設定。")
            else:
                st.warning('請先選擇咖啡風味後再提交紀錄。')

    def _get_brand_options_from_db(self):
        """從資料庫讀取品牌選項"""
        brand_options = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DISTINCT coffee_brand FROM coffee_records;")  # 查詢資料庫中所有不重複的咖啡品牌
                brand_results = cursor.fetchall()
                brand_options = [row[0] for row in brand_results if row[0]]  # 從查詢結果中提取品牌名稱，並排除 None 值
            except Exception as e:
                st.error(f"讀取品牌選項時發生錯誤：{e}")
        return brand_options

    def _get_origin_options_from_db(self):
        """從資料庫讀取產地選項"""
        origin_options = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DISTINCT coffee_origin FROM coffee_records;")  # 查詢資料庫中所有不重複的咖啡產地
                origin_results = cursor.fetchall()
                origin_options = [row[0] for row in origin_results if row[0]]  # 從查詢結果中提取產地名稱，並排除 None 值
            except Exception as e:
                st.error(f"讀取產地選項時發生錯誤：{e}")
        return origin_options


class RecordDisplay:
    """處理歷史紀錄顯示頁面"""
    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.conn = self.db_connector.get_connection() # 取得資料庫連線

    def show_history_page(self):
        """顯示歷史紀錄頁面"""
        st.title('咖啡品嚐紀錄列表 (Neon 資料庫)')
        # 從 Neon 資料庫讀取資料並顯示
        if self.conn:  # 檢查資料庫連線是否建立成功
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM coffee_records ORDER BY id DESC;")  # 讀取所有紀錄，依 id 降序排列
                records = cursor.fetchall()  # 獲取所有查詢結果
                column_names = [desc[0] for desc in cursor.description]  # 從 cursor.description 取得欄位名稱列表

                if records:
                    for record in records:
                        # 動態建立 record_dict，根據欄位名稱取值
                        record_dict = {}
                        for i, col_name in enumerate(column_names):  # 迭代欄位名稱列表和索引
                            record_dict[col_name] = record[i]  # 使用欄位名稱作為 key，索引 i 取值

                        st.subheader(f"**{record_dict['coffee_name']}** (ID: {record_dict['id']})")  # 顯示紀錄 ID
                        st.write(f"**品嚐日期:** {record_dict['record_date']}") # 顯示日期
                        st.write(f"**咖啡品牌:** {record_dict['coffee_brand']}")  # 顯示咖啡品牌
                        st.write(f"**咖啡產地:** {record_dict['coffee_origin']}")  # 顯示咖啡產地
                        st.write(f"**烘焙程度:** {record_dict['roast_level']}")  # 顯示字串形式的烘焙程度
                        st.write(f"**酸度:** {record_dict['acidity_level']}")  # 顯示酸度
                        st.write(f"**苦度:** {record_dict['bitterness_level']}")  # 顯示苦度
                        st.write(f"**品嚐筆記:** {record_dict['taste_notes']}")
                        st.write(f"**咖啡風味:** {record_dict['coffee_flavors']}")
                        rating_stars = "⭐" * (int(record_dict['coffee_rating']) if record_dict['coffee_rating'] else 0)  # 使用欄位名稱 'coffee_rating'，並轉換為整數
                        rating_display = rating_stars if rating_stars else '尚未評分'
                        st.write(f"**咖啡評分:** {rating_display}")
                        st.write('---')
                else:
                    st.info('Neon 資料庫中目前還沒有任何咖啡品嚐紀錄。')
            except Exception as e:
                st.error(f"讀取資料庫發生錯誤：{e}")
        else:
            st.error("無法連線到資料庫，請檢查連線設定。")


if __name__ == '__main__':
    st.set_page_config(page_title="咖啡品嚐紀錄 App", page_icon="☕")

    # 初始化資料庫連線
    db_key = db_setting.DbSetting()
    db_connector = DatabaseConnector(db_key.get_db_setting())

    # 初始化風味資料處理器
    flavor_handler = FlavorDataHandler('flavors_zh_tw.json')

    # 初始化 RecordForm 和 RecordDisplay 物件
    record_form = RecordForm(db_connector, flavor_handler)
    record_display = RecordDisplay(db_connector)


    if 'coffee_records' not in st.session_state:
        st.session_state.coffee_records = []
    if 'selected_flavors' not in st.session_state:
        st.session_state.selected_flavors = []

    # --- Sidebar Navigation ---
    st.sidebar.title('導航')  # Sidebar 標題
    page = st.sidebar.radio("選擇頁面", ["新增紀錄", "歷史紀錄"])  # Sidebar Radio Button 選項

    if page == "新增紀錄":
        record_form.show_add_record_page()
    elif page == "歷史紀錄":
        record_display.show_history_page()

    # 關閉資料庫連線 (在應用程式結束時關閉連線 - Streamlit 應用程式通常長時間運行，可以省略)
    # if conn:
    #     conn.close()