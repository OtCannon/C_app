flavor_categories = {
    "Fruity": ["Citrus fruit", "Dried fruit", "Berry"],
    "Floral": [],  # <--- **[需要您補充: 花香類別的第二層子類別]**
    "Sweet": ["Sweet Aromatics", "Overall Sweet"],
    "Roasted": [], # <--- **[需要您補充: 烘焙類別的第二層子類別，例如 Cereal, Burnt, Tobacco 等，請根據您的風味輪圖片補充]**
    "Sour/Fermented": ["Sour Aromatics", "Alcohol/Fermented", "Acid"],
    "Green/Vegetative": ["Vegetative", "Herb-like"],
    "Other": ["Pungent", "Chemical"]
    # <--- **[請您確認是否需要加入 Nutty/Cocoa 和 Spices 這兩個主要類別，如果需要，請在這裡新增]**
}

flavor_details = {
    "Citrus fruit": ["Lime", "Lemon", "Orange", "Grapefruit"],
    "Dried fruit": ["Peach", "Pear", "Apple", "Pineapple", "Pomegranate"],
    "Berry": ["Cherry", "Coconut", "Prune", "Raisin"],
    "Sweet Aromatics": ["Black Tea", "Vanilla", "Brown Sugar"],
    "Overall Sweet": ["Caramelized", "Honey", "Maple syrup", "Molasses"],
    # <--- **[如果 Roasted 的第二層子類別包含 Cereal, Burnt, Tobacco 等，請在這裡補充它們的第三層詳細描述]**
    # 例如:
    # "Cereal": ["...", "..."],
    # "Burnt": ["...", "..."],
    # "Tobacco": ["...", "..."],
    "Sour Aromatics": ["Lime", "Lemon", "Orange", "Grapefruit"], # <--- **[注意: 與 Citrus fruit 的第三層重複，您可能需要調整分類]**
    "Alcohol/Fermented": ["Winey", "Whiskey", "Fermented", "Overripe"],
    "Acid": ["Acetic acid", "Citric acid", "Malic acid", "Butyric acid", "Isovaleric acid"],
    "Vegetative": ["Dark green", "Fresh", "Under-ripe", "Raw"],
    "Herb-like": ["Olive oil", "Kao", "..."], # <--- **[注意: "Kao" 可能是文字辨識錯誤，請您確認，並補充 Herb-like 可能遺漏的描述]**
    "Pungent": ["Ashy", "Acrid", "Skunky"],
    "Chemical": ["Medicinal", "Salty", "Bitter", "Rubbery", "Petroleum", "Cardboard", "Stale"]
    # <--- **[請您檢查 Other 類別是否還有其他第二層子類別或第三層詳細描述需要補充]**
}

