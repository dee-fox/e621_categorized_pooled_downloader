# e621_categorized_pooled_downloader
## Requirements
<a href=https://github.com/tracer755/e621-wrappers>Python e621 API wrapper<a>

<a href=https://www.python.org>Python >=3.11<a>

<a href=https://pypi.org/project/requests/>Requests<a>
## How to use
Run main.py. The first question you'll be asked is your search query. The second is what tags you need to separate into folders.
The third is a rating threshold (if the post doesn't meet it, it won't be downloaded).
If required, uncomment the login line and put a username and API key there.

## Troubleshooting
### No module named 'e621_endpoints'
Copy the file named that from <a href=https://github.com/tracer755/e621-wrappers>this package<a>'s folder to the folder you're running main.py from.
