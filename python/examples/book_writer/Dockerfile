FROM python:3.10.1
# python:3.10.0 works with otcic but does not export


# Working directory
WORKDIR /book_writer

# Copy otcic and install
COPY ./otcic ./otcic
RUN pip install -e ./otcic --upgrade

# Install other dependencies
COPY ./requirements.txt /book_writer
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy python file
COPY examples/book_writer /book_writer

CMD ["python3", "app.py"]