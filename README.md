
# Stream event generator

Simple event stream generator. The velocity at which events are generated is configurable.
The payload data is generated in the method `get_payload`.
The payload is sent to a AQMP queue (e.g. rabbitmq).


## Deployment of queue in docker container
`docker network create streaming-app-net`

`docker run -v etc/rabbitmq:/etc/rabbitmq \
-e RABBITMQ_DEFAULT_USER=test-user \
-e RABBITMQ_DEFAULT_PASS=test-user \
-p 5672:5672 \
-d --hostname rabbitmq --name rabbitmq -p 8080:15672 --network streaming-app-net --network-alias rabbitmq rabbitmq:3-management`


## Run
- [] optional setup new virtual env, install dependent python libraries
- [] configure `env.template` with credentials to queue.
- [] run `event_generator.py`
