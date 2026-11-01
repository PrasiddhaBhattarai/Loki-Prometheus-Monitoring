#!/bin/bash
set -euo pipefail
export AWS_DEFAULT_REGION=us-east-1   
cd /opt/monitoring

get_param() {
  aws ssm get-parameter --name "$1" --with-decryption \
    --query Parameter.Value --output text
}

export SLACK_WEBHOOK_URL_devops="$(get_param /monitoring/slack_webhook_url_devops)"
export SLACK_WEBHOOK_URL_devs="$(get_param /monitoring/slack_webhook_url_devs)"

# Only substitute our two variables, so any other $ in the file is left alone
envsubst '${slack_webhook_url_devops} ${slack_webhook_url_devs}' \
  < alertmanager/alertmanager.yml.tpl > alertmanager/alertmanager.yml
chown 65534:65534 alertmanager/alertmanager.yml   # alertmanager runs as "nobody"
chmod 600 alertmanager/alertmanager.yml

docker compose up -d --build --force-recreate --remove-orphans