from nosync import db_setting

db_setup = db_setting.DbSetting()
key = db_setup.get_db_setting()

print(key)

