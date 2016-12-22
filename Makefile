DOCKER_REGISTRY ?= registry.honestbee.com
SHORT_NAME ?= coreos-updatenotice
BUILD_TAG ?= git-$(shell git rev-parse --short HEAD)
DEPLOYMENT ?= ${SHORT_NAME}

include versioning.mk

build: docker-build
login: docker-login
push: docker-push
deploy: kube-deploy

docker-build:
ifndef TRAVIS
	docker-compose build
else
	docker build --rm ${MUTABLE_IMAGE} .
endif
	docker tag ${MUTABLE_IMAGE} ${IMAGE}

docker-login:
	@docker login -u="${DOCKER_USERNAME}" -p="${DOCKER_PASSWORD}" ${DOCKER_REGISTRY}

kube-deploy:
	kubectl set image ${DEPLOYMENT} ${SHORT_NAME}=${IMAGE}
