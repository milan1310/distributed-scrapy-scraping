from collections import defaultdict
import datetime
import time
from celery_app import app
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import Session
from models import SpiderTask, SpiderLog, SpiderStatus
from db import SessionLocal
import logging
from scrapy import signals
@app.task(bind=True)
def run_spider(self, task_id, output_file='output.csv'):
    session = SessionLocal()
    task = session.query(SpiderTask).get(task_id)
    if not task:
        return "Task not found"

    task.status = SpiderStatus.RUNNING
    session.commit()

    settings = get_project_settings()
    settings.set('FEED_URI', output_file, priority='cmdline')
    settings.set('FEED_FORMAT', 'csv', priority='cmdline')

    process = CrawlerProcess(settings)
    spider_cls = get_spider_class(task.spider_name)
    crawler = process.create_crawler(spider_cls)

    # Initialize counters
    total_urls_scraped = 0
    successful_requests = 0
    failed_requests = 0
    status_codes = defaultdict(int)
    start_time = time.time()

    def spider_callback(spider, reason):
        end_time = time.time()
        duration = end_time - start_time
        task.status = SpiderStatus.COMPLETED if reason == 'finished' else SpiderStatus.FAILED
        session.commit()

        log = SpiderLog(
            task_id=task_id,
            log_message=f"Spider finished with reason: {reason}",
            total_urls_scraped=total_urls_scraped,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            status_codes=dict(status_codes),
            start_time=datetime.datetime.fromtimestamp(start_time),
            end_time=datetime.datetime.fromtimestamp(end_time),
            duration=duration
        )
        session.add(log)
        session.commit()
        session.close()

    def request_succeeded(response, request, spider):
        nonlocal total_urls_scraped, successful_requests
        total_urls_scraped += 1
        successful_requests += 1
        status_codes[response.status] += 1

    def request_failed(failure, request, spider):
        nonlocal total_urls_scraped, failed_requests
        total_urls_scraped += 1
        failed_requests += 1
        status_codes[500] += 1  # Assuming failure status code as 500

    crawler.signals.connect(request_succeeded, signal=signals.response_received)
    crawler.signals.connect(request_failed, signal=signals.request_dropped)
    crawler.signals.connect(spider_callback, signal=signals.spider_closed)
    process.crawl(crawler, asin=task.start_url)
    process.start(stop_after_crawl=True)

    session.close()

def get_spider_class(spider_name):
    # Import the spider dynamically
    import importlib
    module = importlib.import_module(f"amazon_distribution.spiders.{spider_name}")
    return getattr(module, spider_name.capitalize())
