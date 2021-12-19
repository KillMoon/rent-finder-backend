.PHONY: all
.DEFAULT_GOAL := help

# ----------------------------------------------------------------------------
# Local Variables
#
# ============================================================================

CLIENT=rent-checker
DOCKER_REGISTRY=965067289393.dkr.ecr.us-west-2.amazonaws.com/rent-checker/backend
AWS_REGION=us-west-2

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "⚡ \033[34m%-30s\033[0m %s\n", $$1, $$2}'

all: build push

# ----------------------------------------------------------------------------
# OPTIONAL Commands (helper calls, unrelated to terraform)
#
# ============================================================================

randpass: ## Generate random password
	openssl rand -base64 16

whoami: ## IAM Who Am I?
	aws sts get-caller-identity

# ----------------------------------------------------------------------------
# Build/ECR/Docker Helper Commands
#
# ============================================================================

ecr_login: ## Login to ECR Docker Registry
	aws ecr get-login-password | docker login -u AWS --password-stdin https://${DOCKER_REGISTRY}

ecr_public_login: ## Login to Public ECR Docker Registry
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

build: ecr_public_login ## Build image with paketo, use VERSION
	pack build --path . \
		--builder=public.ecr.aws/saritasa/buildpacks/google/builder:v1 \
		--run-image public.ecr.aws/saritasa/buildpacks/google/runner:v1 \
		${CLIENT}-backend:${VERSION}

	docker tag ${CLIENT}-backend:${VERSION} ${DOCKER_REGISTRY}:${VERSION}

push: ecr_login ## Push built image to ECR, use VERSION
	docker push ${DOCKER_REGISTRY}:${VERSION}
