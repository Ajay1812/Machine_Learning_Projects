# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class ScrapejnmarketPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('myJnmarket.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS jnmarket_table""")
        self.curr.execute("""
                        CREATE TABLE jnmarket_table(
                        name VARCHAR(255),
                        origin VARCHAR(255),
                        price DECIMAL(10,2),
                        specification TEXT,
                        date DATE
                        )""")


    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""INSERT INTO jnmarket_table VALUES(?,?,?,?,?)""",(
            item['name'][0],
            item['origin'][0],
            item['price'][0],
            item['specification'][0],
            item['date']
        ))
        self.conn.commit()
