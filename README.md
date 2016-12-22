# CoreOS Update Notice

This python script will query CoreOS Release channels and store the result to 
Redis. It also supports the ability to call a webhook when a field in the
release information changed.

## Demo

[![asciicast](https://asciinema.org/a/0145x7whsewmrg2t3f3b1lgj1.png)](https://asciinema.org/a/0145x7whsewmrg2t3f3b1lgj1)

## Parameters

| Parameter         | Description                                                  | Default           |
| ----------------- | ------------------------------------------------------------ | ----------------- |
| `REDIS_HOST`      | hostname of redis instance                                   | redis             |
| `REDIS_PORT`      | port of redis service                                        | 6379              | 
| `WEBHOOK_URL`     | if defined, url to post JSON object to                       | ''                |
| `WEBHOOK_KEY`     | Key to compare on, if no difference, webhook won't be called | COREOS_VERSION    |
| `COREOS_CHANNELS` | comma separated list of all channels to check                | stable,beta,alpha |

## Run with Docker-Compose

Use docker-compose to run and test the job.

```bash
docker-compose up -d
```

See logs of the `test-webhook` server
```bash
docker-compose logs test-webhook
```

Re-run the job to confirm webhook is not called when no changes are detected
```bash
docker-compose run job
```

Change the stored release to trigger a change on next job run
```bash
docker-compose exec redis redis-cli
>hset coreos:alpha COREOS_VERSION 1
```

