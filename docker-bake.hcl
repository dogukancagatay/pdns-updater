variable "TAG" {
    default = "latest"
}

variable "IMAGE_NAME" {
    default = "dcagatay/pdns-updater"
}

group "default" {
    targets = [ "app" ]
}

target "app" {
    context = "."
    platforms = [ "linux/amd64", "linux/arm/v7", "linux/arm64/v8" ]
    dockerfile = "Dockerfile"
    tags = [
        "docker.io/${IMAGE_NAME}:${TAG}"
    ]
}
