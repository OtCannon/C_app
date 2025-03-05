import streamlit as st

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
roast_level = st.selectbox('烘焙程度', ['淺焙', '中焙', '深焙'])


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
    st.write('**烘焙程度:**', roast_level)
    st.write('**品嚐筆記:**', taste_notes)
    st.write('**咖啡風味:**', st.session_state.selected_flavors)
    if feedback: # 檢查 feedback 物件是否為 None (使用者是否已評分)
        st.write('**咖啡評分:**', feedback) # 顯示 feedback 中的評分
    else:
        st.write('**咖啡評分:** 尚未評分') # 如果沒有評分，顯示 "尚未評分"
    st.write('---')
    st.write('紀錄已新增！ (目前僅為顯示，尚未儲存)')


if st.button('提交紀錄'):
    if st.session_state.selected_flavors:
        submitted_record = {
            '咖啡名稱': coffee_name,
            '烘焙程度': roast_level,
            '品嚐筆記': taste_notes,
            '咖啡風味': st.session_state.selected_flavors,
            '咖啡評分': feedback if feedback else None # 儲存 feedback 中的評分
        }
        st.session_state.coffee_records.append(submitted_record)
        st.success('品嚐紀錄已提交並儲存！')
        st.session_state.selected_flavors = []
    else:
        st.warning('請先選擇咖啡風味後再提交紀錄。')


st.header('咖啡品嚐紀錄列表')
if st.session_state.coffee_records:
    for record in st.session_state.coffee_records:
        st.subheader(f"**{record['咖啡名稱']}**")
        st.write(f"**烘焙程度:** {record['烘焙程度']}")
        st.write(f"**品嚐筆記:** {record['品嚐筆記']}")
        st.write(f"**咖啡風味:** {', '.join(record['咖啡風味'])}")
        st.write(f"**咖啡評分:** {record['咖啡評分'] if record['咖啡評分'] else '尚未評分'}") # 顯示咖啡評分，若為 None 則顯示 "尚未評分"
        st.write('---')
else:
    st.info('目前還沒有任何咖啡品嚐紀錄。')