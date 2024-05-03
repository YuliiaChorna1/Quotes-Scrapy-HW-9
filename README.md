## Quotes Scrapy with MongoDB and Redis

This project demonstrates scraping quotes and author details from a website, storing them in MongoDB, and offering a command-line interface to query them.
The project consists of several Python modules for scraping quotes, storing them in MongoDB, and offering a command-line interface to query them.

**1. Scrapy Spider:**

* `main.py` defines the Scrapy spider logic for:
  * Scraping quotes and author details from [https://quotes.toscrape.com](https://quotes.toscrape.com).
  * Storing scraped data in JSON files (`quotes.json` and `authors.json`).

**2. Data Model:**

* `models.py` defines the data model for quotes and authors using MongoEngine:
  * `Quotes` document with fields for tags (list of `Tag` objects), author (reference to `Authors` document), and quote text.
  * `Authors` document with fields for full name, born date, born location, and description.
  * `Tag` embedded document with a name field.

**3. Data Seeding:**

* `seed.py` provides functionalities for loading scraped data (from JSON files) and populating the MongoDB database:
  * `DataLoader` class loads JSON data from a file.  
  * `DataSeeder` class populates the `Authors` and `Quotes` collections with the loaded data.

**4. Data Provider and Manager:**

* `bot.py` implements the data provider and manager for the quote bot:
  * `DataProvider` abstract class defines the interface for querying quotes by author or tags.
  * `MongoDataProvider` class provides concrete implementation using MongoEngine queries.
  * `DataManager` class manages the data provider and caches queries using `redis-lru` for performance.

**5. Command-Line Bot:**

* `bot.py` also defines the command-line interface logic:
  * `CommandManager` class handles user commands for querying quotes and provides help information.
  * The main function creates a `CommandManager` instance and runs a loop to:
    * Print help at startup.
    * Prompt the user for input.
    * Handle user input using the `CommandManager`.
    * Exit the loop on exit commands.

**6. Additional Notes:**

* `connect.py` establishes a connection to the MongoDB cluster using configuration from `config.ini`.


### Dependencies

* Scrapy
* MongoEngine
* Redis
* redis-lru

### Setup

1. Install required dependencies.
2. Configure MongoDB connection details in `config.ini`.

### Running the Scraper

```bash
python main.py
```

This will scrape quotes and authors from the website and save them to JSON files.

### Seeding the Database

```bash
python seed.py
```

This will load the scraped data from JSON files and populate the MongoDB database.

### Running the Quote Bot

```bash
python bot.py
```

This will start the command-line interface where you can query quotes using commands like:

* `name: [author name]` - Get quotes by author name.
* `tag: [tag]` - Get quotes by a tag.
* `tags: [tag-1],[tag-2],...,[tag-n]` - Get quotes with all the specified tags.
