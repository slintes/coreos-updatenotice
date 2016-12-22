MUTABLE_VERSION ?= latest

IMAGE := ${DOCKER_REGISTRY}/${SHORT_NAME}:${BUILD_TAG}
MUTABLE_IMAGE := ${DOCKER_REGISTRY}/${SHORT_NAME}:${MUTABLE_VERSION}

info:
	@echo "Build tag:      ${BUILD_TAG}"
	@echo "Registry:       ${DOCKER_REGISTRY}"
	@echo "Immutable tag:  ${IMAGE}"
	@echo "Mutable tag:    ${MUTABLE_IMAGE}"

.PHONY: docker-push
docker-push: docker-mutable-push docker-immutable-push

.PHONY: docker-immutable-push
docker-immutable-push:
	docker push ${IMAGE}

.PHONY: docker-mutable-push
docker-mutable-push:
	docker push ${MUTABLE_IMAGE}
