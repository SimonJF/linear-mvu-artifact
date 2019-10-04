FROM ocaml/opam2:alpine-3.10-ocaml-4.08
WORKDIR /home/opam
ADD links links
ADD opam-repository opam-repository-snapshot
ADD run-chatserver.sh run-chatserver.sh
ADD run-two-factor.sh run-two-factor.sh
ADD run-pingpong.sh run-pingpong.sh
ADD run-example.py run-example.py
ADD examples examples
ADD config config
USER root
WORKDIR /root
RUN apk update && apk upgrade && \
	apk add coreutils && \
	apk add camlp4 m4 libressl-dev && \
  apk add python2 && \
  apk add python3 && \
	chown opam:nogroup -R /home/opam/links
USER opam
WORKDIR /home/opam/links
RUN \
  opam repository set-url default /home/opam/opam-repository-snapshot && \
  opam update && \
  opam install -y dune
RUN	eval `opam config env` && \
	opam pin add links . -y && \
	make nc && \
	sudo ln -s /home/opam/links/linx /usr/local/bin/
WORKDIR /home/opam/
EXPOSE 8080
CMD [ "bash" ]
