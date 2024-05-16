# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3


class MongodbPipeline(object):
    collect_name = "best_movies"
    
    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))
        
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://admin:admin1@cluster0.s8rdbyy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client["IMDB"]
        
    def close_spider(self, spider):
        self.client.close()
        
    def process_item(self, item, spider):
        self.db[self.collect_name].insert_one(item)
        return item
 
    
class SQLlitePipeline(object):
    
    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))
        
    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute(
                '''
                CREATE TABLE IF NOT EXISTS best_movies(
                    title TEXT,
                    year TEXT,
                    duration TEXT,
                    genre TEXT,
                    rating TEXT,
                    movie_url TEXT
                )
                '''
            )
            self.connection.commit()
        except sqlite3.OperationalError:
            pass
        
    def close_spider(self, spider):
        self.connection.close()
        
    def process_item(self, item, spider):
        try:
            # Ensure 'genre' is a string
            genre = ', '.join(item.get('genre')) if isinstance(item.get('genre'), list) else item.get('genre')

            self.c.execute(
                '''
                INSERT INTO best_movies (title, year, duration, genre, rating, movie_url)
                VALUES (?,?,?,?,?,?)
                ''',
                (item.get('title'), item.get('year'), item.get('duration'), genre, item.get('rating'), item.get('movie_url'))
            )
            self.connection.commit()
        except sqlite3.Error as e:
            logging.error(f"Error inserting item: {e}")
        return item

