import streamlit as st
import psycopg2  # 導入 psycopg2 函式庫
import os # 導入 os 模組

from nosync import db_setting

# Neon 資料庫設定
db_init = db_setting.DbSetting()
DATABASE_URL = db_init.get_db_setting() # 替換成您的 Neon 資料庫連線 URL

# 初始化資料庫連線 (在應用程式啟動時建立連線)
def init_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        st.error(f"資料庫連線錯誤：{e}")
        return None

conn = init_db_connection() # 建立資料庫連線


if 'coffee_records' not in st.session_state:
    st.session_state.coffee_records = []
if 'selected_flavors' not in st.session_state:
    st.session_state.selected_flavors = []

flavor_categories = { # Your flavor categories dictionary
    "Fruity": ["Citrus fruit", "Dried fruit", "Berry", "Other fruit"],
    "Floral": ["Floral", "Black tea"],
    "Sweet": ["Sweet Aromatics", "Overall Sweet", "Vanillin", "Vanilla", "Brown sugar"],
    "Nutty/Cocoa": ["Nutty", "Cocoa",],
    "Spices": ["Pungent", "Brown spice", "Pepper"],
    "Roasted": ["Cereal", "Burnt", "Tobacco", "Pipe tobacco"],
    "Sour/Fermented": ["Sour Aromatics", "Alcohol/Fermented"],
    "Green/Vegetative": ["Olive Oil","Raw","Green/Vegetative", "Beany"],
    "Other": ["Papery/Musty", "Chemical"]
}

flavor_details = { # Your flavor details dictionary
    "Citrus fruit": ["Lime", "Lemon", "Orange", "Grapefruit"],
    "Dried fruit": ["Raisin","Prune"],
    "Berry": ["Blackberry", "Raspberry", "Strawberry","Blueberry"],
    "Other fruit": ["Coconut", "Cherry", "Pineapple", "Grape", "Apple", "Peach", "Pear", "Pomegranate"],
    "Floral": ["Jasmine", "Chamomile", "Rose"],
    "Black tea": ["Black tea", "Green tea"],
    "Brown sugar": ["Honey", "Caramelized", "Maple syrup", "Molasses"],
    "Cocoa": ["Chocolate", "Dark chocolate", "Milk chocolate"],
    "Nutty": ["Peanut", "Almond", "Hazelnut"],
    "Cereal": ["Grain", "Malt"],
    "Burnt": ["Brown, Roast", "Smoky", "Ashy", "Acrid"],
    "Chemical": ["Bitter", "Salty", "Medicinal", "Petroleum", "Skunky", "Rubber"],
    "Papery/Musty": ["Phenolic", "Meaty/Brothy", "Animalic", "Musty/Earthy", "Musty/Dusty", "Moldy/Damp", "Woody", "Papery", "Cardboard", "Stale"],
    "Green/Vegetative": ["Fresh", "Under-ripe", "Peapod", "Dark green", "Vegetative", "Hay-like", "Herb-like"],
    "Alcohol/Fermented": ["Whiskey", "Winey", "Fermented", "Overripe"],
}


st.title('Record Notes')
st.write('Add your coffee tasting notes here!')

coffee_name = st.text_input('咖啡名稱')
# 將烘焙程度改為滑桿 (範圍 1-10)
roast_level = st.slider('烘焙程度 (1-10)', 1, 10, 5) # 預設值設為 5
# 增加酸度滑桿 (範圍 1-10)
acidity_level = st.slider('酸度 (1-10)', 1, 10, 5) # 預設值設為 5
# 增加苦度滑桿 (範圍 1-10)
bitterness_level = st.slider('苦度 (1-10)', 1, 10, 5) # 預設值設為 5

st.write('Rating')
feedback = st.feedback(
    options="stars",
    key="coffee_rating_feedback",
)# 為 feedback 元件設定一個唯一的 key

st.header('選擇咖啡風味 (三層選單)')

primary_category_options = list(flavor_categories.keys())
selected_primary_category = st.multiselect("主要風味類別 (第一層)", primary_category_options)

subcategory_options = []
if selected_primary_category:
    for category in selected_primary_category: # Iterate through selected primary categories
        subcategory_options.extend(flavor_categories[category]) # Add subcategories from each selected category
selected_subcategory = st.multiselect("次要風味類別 (第二層)", subcategory_options)

detail_flavor_options = []
if selected_subcategory:
    for subcategory in selected_subcategory: # Iterate through selected subcategories
        if subcategory in flavor_details: # Check if subcategory has details in flavor_details dictionary
            detail_flavor_options.extend(flavor_details[subcategory]) # Add details for each selected subcategory
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
st.session_state.selected_flavors = all_selected_flavors # Update session state with combined selections

# Display currently selected flavors
if st.button('顯示紀錄'):
    st.write('---')
    st.write('**咖啡名稱:**', coffee_name)
    # 顯示滑桿數值
    st.write('**烘焙程度:**', roast_level)
    st.write('**酸度:**', acidity_level)
    st.write('**苦度:**', bitterness_level)
    st.write('**品嚐筆記:**', taste_notes)
    st.write('**咖啡風味:**', st.session_state.selected_flavors)
    if feedback is not None: # 檢查 feedback 物件和評分值是否存在
        st.write('**咖啡評分:**',  "⭐" * feedback) # 顯示 feedback 中的星級評分 (星星符號)
    else:
        st.write('**咖啡評分:** 尚未評分') # 如果沒有評分，顯示 "尚未評分"
    st.write('---')
    st.write('紀錄已新增！ (目前僅為顯示，尚未儲存)')


if st.button('提交紀錄'):
    if st.session_state.selected_flavors:
        if conn: # 檢查資料庫連線是否建立成功
            try:
                cursor = conn.cursor()
                # 建立資料表欄位 (如果不存在) - 只需執行一次 (為了新增 acidity_level 和 bitterness_level 欄位)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS coffee_records (
                        id SERIAL PRIMARY KEY,
                        coffee_name VARCHAR(255),
                        roast_level VARCHAR(50),  -- 烘焙程度改為數值，但資料庫欄位型態先保持 VARCHAR
                        acidity_level INTEGER,     -- 新增酸度欄位 (整數)
                        bitterness_level INTEGER,  -- 新增苦度欄位 (整數)
                        taste_notes TEXT,
                        coffee_flavors VARCHAR(255),
                        coffee_rating INTEGER
                    );
                """)
                conn.commit() # 提交資料表結構變更

                # 將風味列表轉換為逗號分隔的字串
                flavor_string = ", ".join(st.session_state.selected_flavors)
                rating_value = feedback.get("rating") if feedback and feedback.get("rating") else None # 取得評分值，沒有評分則為 None

                # 插入資料到資料庫 (包含 roast_level, acidity_level, bitterness_level)
                cursor.execute("""
                    INSERT INTO coffee_records (coffee_name, roast_level, acidity_level, bitterness_level, taste_notes, coffee_flavors, coffee_rating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (coffee_name, str(roast_level), acidity_level, bitterness_level, taste_notes, flavor_string, rating_value)) # roast_level 轉為字串儲存
                conn.commit() # 提交資料插入

                st.success('品嚐紀錄已提交並儲存到 Neon 資料庫！')
                st.session_state.coffee_records = [] # 清空 session_state 中的紀錄
                st.session_state.selected_flavors = []
            else:
                st.error("database error")
        else:
            st.error("無法連線到資料庫，請檢查連線設定。")
    else:
        st.warning('請先選擇咖啡風味後再提交紀錄。')


    st.header('咖啡品嚐紀錄列表 (Neon 資料庫)')
    # 從 Neon 資料庫讀取資料並顯示
    if conn: # 檢查資料庫連線是否建立成功
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM coffee_records ORDER BY id DESC;") # 讀取所有紀錄，依 id 降序排列
            records = cursor.fetchall() # 獲取所有查詢結果

            if records:
                for record in records:
                    record_dict = { # 將資料庫 tuple 轉換為 dictionary，方便使用欄位名稱
                        'id': record[0],
                        '咖啡名稱': record[1],
                        '烘焙程度': record[2], # 資料庫中 roast_level 仍為字串
                        '酸度': record[3],      # 新增酸度
                        '苦度': record[4],      # 新增苦度
                        '品嚐筆記': record[5],
                        '咖啡風味': record[6],
                        '咖啡評分': record[7]
                    }
                    st.subheader(f"**{record_dict['咖啡名稱']}** (ID: {record_dict['id']})") # 顯示紀錄 ID
                    st.write(f"**烘焙程度:** {record_dict['烘焙程度']}") # 顯示字串形式的烘焙程度
                    st.write(f"**酸度:** {record_dict['酸度']}")          # 顯示酸度
                    st.write(f"**苦度:** {record_dict['苦度']}")          # 顯示苦度
                    st.write(f"**品嚐筆記:** {record_dict['品嚐筆記']}")
                    st.write(f"**咖啡風味:** {record_dict['咖啡風味']}")
                    rating_stars = "⭐" * (record_dict['咖啡評分'] if record_dict['咖啡評分'] else 0) # 將數字評分轉換為星星符號
                    rating_display = rating_stars if rating_stars else '尚未評分' # 如果沒有評分，顯示 "尚未評分"
                    st.write(f"**咖啡評分:** {rating_display}")
                    st.write('---')
            else:
                st.info('Neon 資料庫中目前還沒有任何咖啡品嚐紀錄。')
        except Exception as e:
            st.error(f"讀取資料庫發生錯誤：{e}")
    else:
        st.error("無法連線到資料庫，請檢查連線設定。")


    # 關閉資料庫連線 (在應用程式結束時關閉連線 - Streamlit 應用程式通常長時間運行，可以省略)
    # if conn:
    #     conn.close()