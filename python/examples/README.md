# Examples

Here are some examples demonstrating how OTCIC can be used with Python applications. Ensure that you have all dependencies installed in the `requirements.txt` file. The use of Conda environments is recommended. 

To install all dependencies with Conda use:
```
conda create -n otcic --file python/requirements.txt
```

To install dependencies with pip:
```
pip install -r python/requirements.txt
pip install -e python/otcic
```

## HTTP Server

This is a simple HTTP web server powered by Flask. To run the example use:
```
flask --app python/examples/http_server/app.py run
```

When running the server, you can go to 3 links:

Server ADD: `localhost:4949/add`
Add a row to a table (simulate increased memory usage).

Server MOD: `localhost:4949/mod`
Modify a random row in the table.

Server DEL: `localhost:4949/del`
Delete a row from the table (simulate decreased memory usage).

If you have the Collector running as described in the parent directory, this will start logging the results to a `metrics.json` file. 
