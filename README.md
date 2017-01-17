This is a fork of https://github.com/honestbee/coreos-updatenotice.
It uses a notification format which can be directy used for Slack Webhooks.

Original Readme:

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

## Kubernetes CronJob

Note: At the time of writing, [CronJob](http://kubernetes.io/docs/user-guide/cron-jobs/) 
is still in Alpha stage. To use it we need to run API Server with alpha features enabled:
```
--runtime-config=batch/v2alpha1
```

If you choose to use a webhook (i.e. [cog trigger](http://cog-book.operable.io/#_triggers)).
Store the reference to the webhook in a configmap:
```
kubectl create cm coreos-updatenotice --from-literal=webhook_url=https://cog.example.com:4001/v1/triggers/00000000-0000-0000-0000-000000000000
```

Create Redis service and deployment 
```
kubectl create -f k8s-manifests/02-redis-svc.yaml
kubectl create -f k8s-manifests/03-redis-deploy.yaml
```

Create CronJob
```
kubectl create -f k8s-manifests/04-cronjob.yaml
```

Enjoy Cog notifications in Slack/HipChat when CoreOS channels change their current version!

