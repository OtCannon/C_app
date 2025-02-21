import streamlit as st

if 'coffee_records' not in st.session_state:
    st.session_state.coffee_records = []

st.title('我的咖啡品嚐記錄網頁')
st.write('歡迎來到您的個人咖啡品嚐記錄網頁！')

st.image('coffee_wheel.png', caption='咖啡風味輪', use_container_width=True)

coffee_name = st.text_input('咖啡名稱')
roast_level = st.selectbox('烘焙程度', ['淺焙', '中焙', '深焙'])
taste_notes = st.text_area('品嚐筆記')

flavor_categories = [
    '果香 (Fruity)', '花香 (Floral)', '甜感 (Sweet)', '堅果/可可 (Nutty/Cocoa)',
    '香料 (Spices)', '烘焙 (Roasted)', '其他 (Other)', '植物/蔬菜 (Green/Vegetative)',
    '酸/發酵 (Sour/Fermented)', '柑橘 (Citrus fruit)', '乾果 (Dried fruit)', '莓果 (Berry)'
]

selected_flavors = st.multiselect('咖啡風味', flavor_categories)

if st.button('新增紀錄'):
    new_record = {  # 建立一個字典來儲存單筆咖啡紀錄
        '咖啡名稱': coffee_name,
        '烘焙程度': roast_level,
        '品嚐筆記': taste_notes,
        '咖啡風味': selected_flavors
    }
    st.session_state.coffee_records.append(new_record) # 將新紀錄加入列表
    st.success('紀錄已新增！') # 使用 st.success 顯示成功訊息，更醒目


st.header('咖啡品嚐紀錄列表') # 加入標題

if st.session_state.coffee_records: # 檢查紀錄列表是否為空
    for record in st.session_state.coffee_records: # 迴圈讀取每一筆紀錄
        st.subheader(f"**{record['咖啡名稱']}**") # 顯示咖啡名稱作為子標題
        st.write(f"**烘焙程度:** {record['烘焙程度']}")
        st.write(f"**品嚐筆記:** {record['品嚐筆記']}")
        st.write(f"**咖啡風味:** {', '.join(record['咖啡風味'])}") # 將風味列表轉換為字串顯示
        st.write('---') # 加入分隔線
else:
    st.info('目前還沒有任何咖啡品嚐紀錄。') # 如果沒有紀錄，顯示提示訊息