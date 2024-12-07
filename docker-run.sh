#!/usr/bin/env bash

set -e

[ ! "$*" ] && echo No command specified && exit 1

cmd=""; for i in "$@"; do cmd="$cmd '$i'"; done

[ -e /.dockerenv ] && exec bash -c "$cmd"

source_dir=$(dirname $(readlink -f $0))
source_dir_name=$(basename $source_dir)

container_name=${CONTAINER_NAME:-$USER-$source_dir_name-pisa}

GID=$(id -g)

if [ ! "$(docker ps -a | grep ${container_name}$)" ]; then
    bash setup.sh
elif [ "$(docker inspect -f '{{.State.Running}}' $container_name)" = "false" ]; then
    docker start $container_name > /dev/null
elif [ "$RESTART" ]; then
    # The container runs "bash" as the entrypoint, and bash in interactive mode ignores the default SIGTERM
    # causing restart to wait 10 extra seconds for the timeout to expire before sending SIGKILL. Instruct it
    # to use SIGKILL directly to speed up the restart.
    docker restart -s KILL $container_name > /dev/null
fi

if [ "$(docker inspect -f '{{.State.Running}}' $container_name)" = "false" ]; then
        echo Cannot start container $container_name
        exit 1
fi

# Keep the container's timezone in sync with the host
docker cp -L /etc/localtime $container_name:/etc/localtime > /dev/null

args=()

[ -t 0 ] && args+=("-it")

docker exec --privileged --user=$UID:$GID ${args[@]} $container_name bash -c "$cmd"
