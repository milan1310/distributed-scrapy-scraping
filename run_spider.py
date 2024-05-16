from db import SessionLocal
from models import SpiderTask
from tasks import run_spider

def create_spider_task(spider_name, start_url):
    session = SessionLocal()
    task = SpiderTask(spider_name=spider_name, start_url=start_url)
    session.add(task)
    session.commit()

    run_spider.delay(task.id)
    session.close()

# Example usage
if __name__ == "__main__":
    create_spider_task("amazonpdp", "NumDVBSA")
