# save-qts

## Requirements

- A computer with macOS, or the knowledge to do this without direct assistance
- `pueue` for task management and log retention
  - Very important, as failures do happen!
  - https://github.com/Nukesor/pueue
- Recent version of Python (preferably Python 3.9)
- Python packages: `scrapy` and `scrapy-splash`
- Splash instance access, or Docker

```
brew install pueue
```
```
python -m venv .venv
pip install scrapy scrapy-splash
source .venv/bin/activate
```

## Running

First, set environment variable secrets.
```
export SPLASH_URL=<secret>
export SPLASH_TOKEN=<secret>
```

Then, run the scrape. Replace `URL_FILE` and `OUTPUT_DIR` with the appropriate files.

`URL_FILE` should contain only URLs to scrape.
```
pueue add -- SCRAPY_SPLASH=1 scrapy crawl -a urls=URL_FILE -a out_dir=OUTPUT_DIR save_qt
```

Once this is done, check the logs for errors. Replace `TASK_ID` with the
appropriate id from `pueue status`.
```
pueue status
pueue log TASK_ID | grep 'Gave up'
```

A scrape with "Gave up" means that you should open the relevant URL in browser.
There's a good chance that it's broken and won't load.

However, if it works in browser, you need to rescrape those URLs. Create a *new*
file with one failed URL per line, and rerun the crawl with that input file.

### Questions?

Good luck.
