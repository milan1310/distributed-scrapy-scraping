# Distributed Scraping Architecture

Welcome to the Distributed Scraping Architecture project! This project leverages Scrapy, Celery, Redis, and scrapy-redis to create a scalable and robust web scraping framework.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Upcoming](#upcoming)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction
In today's data-driven world, efficiently gathering and processing large datasets is crucial. This project aims to provide a distributed web scraping architecture that can handle large-scale data extraction tasks reliably.

## Features
- **Scrapy**: Powerful web crawling and scraping framework.
- **Celery**: Asynchronous task queue/job queue for distributing scraping tasks.
- **Redis**: In-memory data structure store used as a message broker.
- **scrapy-redis**: Integration to distribute Scrapy tasks across multiple nodes.

## Upcoming
- [ ] Adding new way of executing scrapers using `subprocess`
- [ ] Structured way to start distributed scraping for dummys

## Installation
To get started, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/milan1310/distributed-scrapy-scraping.git
cd distributed-scrapy-scraping
pip install -r requirements.txt
```

## Usage
1. **Start Redis**: Make sure you have Redis installed and running.
   ```bash
   redis-server
   ```
2. **Start Celery**: Run Celery worker to process tasks.
   ```bash
   celery -A tasks worker --loglevel=info
   ```
3. **Add URLs to Queue**: Use the `add_urls.py` script to add URLs to the Redis queue.
   ```bash
   python add_urls.py
   ```
4. **Run Spider**: Execute the spider to start scraping.
   ```bash
   python run_spider.py
   ```

## Project Structure
```
distributed-scrapy-scraping/
├── amazon_distribution/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   ├── spiders/
│   │   ├── __init__.py
│   │   └── amazon_spider.py
├── scrapy-redis/
│   ├── __init__.py
│   ├── connection.py
│   ├── defaults.py
│   ├── dupefilter.py
│   ├── picklecompat.py
│   ├── pipeline.py
│   ├── queue.py
│   ├── scheduler.py
├── .gitignore
├── add_urls.py
├── celery_app.py
├── db.py
├── models.py
├── requirements.txt
├── run_spider.py
├── scrapy.cfg
└── tasks.py
```

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests.
