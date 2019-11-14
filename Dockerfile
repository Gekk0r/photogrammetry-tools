FROM ubuntu:14.10

RUN useradd -m -d /home/web web &amp;&amp; mkdir /home/web/.venv &amp;&amp;\


USER web
WORKDIR /home/web
ENV PYTHONPATH /home/web/webapp

COPY webapp /home/web/webapp

ENTRYPOINT ["/home/web/.venv/default/bin/cherryd", "-i", "server"]