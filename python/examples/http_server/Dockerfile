FROM python:3.10.0

# Working directory
WORKDIR /http_server

# Copy otcic and install
COPY ./otcic ./otcic
RUN pip install -e ./otcic

# Install other dependencies
COPY ./requirements.txt /http_server
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy python file
COPY examples/http_server /http_server

# Start HTTP example
CMD ["python3", "-m", "flask", "run"]