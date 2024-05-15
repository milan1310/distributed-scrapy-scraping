from celery_app import app
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import Session
from models import SpiderTask, SpiderLog, SpiderStatus
from db import SessionLocal
import logging
from scrapy import signals
@app.task(bind=True, max_retries=3)
def run_spider(self, task_id):
    session = SessionLocal()
    task = session.query(SpiderTask).get(task_id)
    if not task:
        return "Task not found"

    task.status = SpiderStatus.RUNNING
    session.commit()

    process = CrawlerProcess(get_project_settings())

    def spider_callback(spider, reason):
        task.status = SpiderStatus.COMPLETED if reason == 'finished' else SpiderStatus.FAILED
        session.commit()
        log = SpiderLog(task_id=task_id, log_message=f"Spider finished with reason: {reason}")
        session.add(log)
        session.commit()

    process = CrawlerProcess(get_project_settings())
    spider_cls = get_spider_class(task.spider_name)
    crawler = process.create_crawler(spider_cls)
    crawler.signals.connect(spider_callback, signal=signals.spider_closed)
    process.crawl(crawler, asin=task.start_url)
    process.start()
    # spider_cls = get_spider_class(task.spider_name)
    # process.crawl(spider_cls, start_url=task.start_url)
    # process.signals.connect(spider_callback, signal=scrapy.signals.spider_closed)
    # process.start()

    session.close()

def get_spider_class(spider_name):
    # Import the spider dynamically
    import importlib
    module = importlib.import_module(f"amazon_distribution.spiders.{spider_name}")
    return getattr(module, spider_name.capitalize())
