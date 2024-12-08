#!/usr/bin/env bash

if ! command -v docker &>/dev/null; then
    echo "Docker is not installed"
    exit 1
fi

if ! getent group docker >/dev/null 2>&1; then
    echo "docker group does not exist"
    exit 1
fi

if ! getent group docker | grep &>/dev/null "\b${USER}\b"; then
    echo "Please add user '${USER}' in the docker group. Command: sudo usermod -aG docker ${USER}"
    exit 1
fi

source_dir=$(dirname $(readlink -f $0))
source_dir_name=$(basename $source_dir)

git -C $source_dir submodule update --init --recursive

container_name=${CONTAINER_NAME:-$USER-$source_dir_name-pisa}

if [ "$(docker ps -a -q -f name=${container_name})" ]; then
    echo "Deleting existing container ${container_name}"
    docker rm -f ${container_name}
fi

docker image build \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    -t pisa \
    -f Dockerfile .

docker run -d -it \
    -p 0.0.0.0:80:5000/tcp \
    --name $container_name \
    --hostname $(hostname)-$container_name \
    pisa

GID=$(id -g)

docker exec $container_name bash -c "
    groupadd -f -g $GID $USER &&
    useradd -u $UID -g $GID $USER &&
    mkdir /home/$USER &&
    chown -R $UID:$GID /home/$USER &&
    chown -R $UID:$GID /app &&
    mkdir -p /etc/sudoers.d &&
    echo '$USER ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/$USER"
