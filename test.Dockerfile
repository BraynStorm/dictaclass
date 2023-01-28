ARG PY_VERSION
FROM python:${PY_VERSION}
WORKDIR /x
ADD requirements.*txt /x
RUN pip3 --no-cache-dir install -U -r requirements.dev.txt -r requirements.dev.txt
ADD . /x
CMD [ "python3", "-m", "pytest", "--color=no", "--tb=native" ]
