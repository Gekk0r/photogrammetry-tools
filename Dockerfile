FROM ubuntu:14.10

RUN useradd -m -d /home/web web &amp;&amp; mkdir /home/web/.venv &amp;&amp;\

apt-get update &amp;&amp; sudo apt-get upgrade -y &amp;&amp; \
apt-get install -y libc6 libc6-dev libpython2.7-dev libpq-dev libexpat1-dev libffi-dev libssl-dev python2.7-dev python-pip &amp;&amp; \
pip install virtualenv &amp;&amp; \
virtualenv -p python2.7 /home/web/.venv/default &amp;&amp; \
/home/web/.venv/default/bin/pip install cython &amp;&amp; \
/home/web/.venv/default/bin/pip install cherrypy==3.6.0 pyopenssl mako psycopg2 python-memcached sqlalchemy &amp;&amp; \
apt-get autoclean -y &amp;&amp; \
apt-get autoremove -y &amp;&amp; \
chown -R web.web /home/web/.venv

USER web
WORKDIR /home/web
ENV PYTHONPATH /home/web/webapp

COPY webapp /home/web/webapp

ENTRYPOINT ["/home/web/.venv/default/bin/cherryd", "-i", "server"]