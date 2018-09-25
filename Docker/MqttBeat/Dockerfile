FROM alpine:3.8

RUN apk --no-cache add bash make build-base cmake libc-dev go go-tools glide python2 git openssh-client ca-certificates
RUN python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    pip install virtualenv

ENV GOPATH /go
RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p ${GOPATH}/src/github.com/elastic && \
    git clone https://github.com/elastic/beats ${GOPATH}/src/github.com/elastic/beats
WORKDIR ${GOPATH}/src/github.com/elastic/beats
RUN make; exit 0;

RUN mkdir -p ${GOPATH}/src/github.com/nathan-k-/ && \
    git clone https://github.com/nathan-k-/mqttbeat ${GOPATH}/src/github.com/nathan-k-/mqttbeat
WORKDIR ${GOPATH}/src/github.com/nathan-k-/mqttbeat
RUN glide install && \
    make