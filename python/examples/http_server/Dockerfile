FROM python:3.10.1
# python:3.10.0 works with otcic but does not export


# Working directory
WORKDIR /http_server

# Copy otcic and install
COPY ./otcic ./otcic
RUN pip install -e ./otcic --upgrade

# Install other dependencies
COPY ./requirements.txt /http_server
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy python file
COPY examples/http_server /http_server

# Start HTTP example
#CMD ["python3", "-m", "flask", "run"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
# this will pass through docker, accessible through 127.0.0.1/rolldice
