#!/bin/bash
if [ ! "$(docker images links_mvu | grep links_mvu)" ]; then
	docker build -t links_mvu links-docker
fi
