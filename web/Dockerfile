FROM python:3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install dependencies
RUN apt-get update --fix-missing
RUN apt-get install -y nginx supervisor netcat

# install module dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /usr/local/lib/nltk_data
ENV NLTK_DATA /usr/local/lib/nltk_data
RUN python -m textblob.download_corpora

# copy nginx config to container
ADD nginx.conf /etc/nginx/nginx.conf

# copy local project dir to container
ADD ./ /usr/src/app

# compress css and js files
RUN sh /usr/src/app/compress.sh

# create unprivileged user
RUN adduser --disabled-password --gecos '' guest
RUN chown -R guest /usr/src/app
