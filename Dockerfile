FROM python:3.9.2

LABEL Maintainer="Geophotofinder"

WORKDIR /usr/app/src

COPY *.py ./
COPY requirements.txt ./
COPY test.jpg ./

# Update package list
RUN apt update

# Install necessary packages
RUN apt -y install libexiv2-dev libboost-python-dev python-all-dev g++

# Check pip versions (optional)
RUN pip3 --version | pip --version

# Install Python packages from requirements file
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py"]