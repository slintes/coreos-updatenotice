# CoreOS Update Notice

This python script will query CoreOS Release channels and store the result to 
Redis. It also supports the ability to call a webhook when a field in the
release information changed.

## Parameters

| Parameter         | Description                                                  | Default           |
| ----------------- | ------------------------------------------------------------ | ----------------- |
| `REDIS_HOST`      | hostname of redis instance                                   | redis             |
| `REDIS_PORT`      | port of redis service                                        | 6379              | 
| `WEBHOOK_URL`     | if defined, url to post JSON object to                       | ''                |
| `WEBHOOK_KEY`     | Key to compare on, if no difference, webhook won't be called | COREOS_VERSION    |
| `COREOS_CHANNELS` | comma separated list of all channels to check                | stable,beta,alpha |


