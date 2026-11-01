global:
  resolve_timeout: 5m

route:
  receiver: "slack-dev"
  group_by: ["alertname", "severity"]
  group_wait: 30s
  group_interval: 1m
  repeat_interval: 30m

  routes:
    - matchers:
      - severity="warning"
      receiver: "slack-dev"
      continue: false

    - matchers:
      - severity="critical"
      receiver: "slack-devops"
      continue: false

receivers:
  - name: "slack-dev"
    slack_configs:
      - channel: "#devs-warning"
        send_resolved: true
        username: "Prometheus-bot"
        icon_emoji: ":rotating_light:"
        text: ":rotating_light: {{ .CommonLabels.alertname }} ({{ .CommonLabels.severity }})"
        api_url: ${SLACK_WEBHOOK_URL_devs}

  - name: "slack-devops"
    slack_configs:
      - channel: "#devops-warning"
        send_resolved: true
        username: "Prometheus-bot"
        icon_emoji: ":warning:"
        text: ":warning: {{.CommonLabels.alertname}} ({{.CommonLabels.severity}})"
        api_url: ${SLACK_WEBHOOK_URL_devops}