ARG PYTHON_VERSION=3.10-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

# COPY requirements.txt /tmp/requirements.txt
# RUN set -ex && \
#     pip install --upgrade pip && \
#     pip install -r /tmp/requirements.txt && \
#     rm -rf /root/.cache/

#pip 기본 설정
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY . /code

ENV SECRET_KEY "Bl6Vck5Ra8v2xo39i44ukcoVMrOTbkKK0OAbHrJ8LnR7ourcvW"
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","2","config.wsgi"]
