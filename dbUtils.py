import pymongo


class DBUtils(object):

    def __init__(self):
        self.client = None
        pass

    def db_connect(self):
        try:
            # 连接数据库
            self.client = pymongo.MongoClient('localhost', 27017)
        except:
            exit(1)

    def db_insert_one(self, dict_data):
        try:
            # 获取数据库
            mydb = self.client['spyLianjia']
            # 获取数据集合
            house_info = mydb['houseInfo']
            house_info.insert_one(dict_data)
        except:
            print("数据库插入异常")
            return

    def db_insert_many(self, list_data):
        try:
            # 获取数据库
            mydb = self.client['spyLianjia']
            # 获取数据集合
            house_info = mydb['houseInfo']
            house_info.insert_many(list_data)
        except:
            print("数据库插入异常")
            return

    def db_get_info(self, query_dict):
        try:
            mydb = self.client['spyLianjia']
            # 获取数据集合
            house_info = mydb['houseInfo']
            return house_info.find({}, query_dict)
        except:
            print("读取数据库异常")
            return

    def db_close(self):
        try:
            self.client.close()
        except:
            print('数据库关闭连接异常')
            return
