# Milestone 21 - Logging (Loki + Promtail)

## Objective

Add centralized, searchable logging to the platform with **Loki + Promtail**, and
surface it in the **same Grafana** already used for metrics. Every pod's logs are
collected cluster-wide and queryable with LogQL, so debugging no longer means
`kubectl logs` pod-by-pod — and short-lived pods (Kubeflow steps, the model-refresh
CronJob, KServe pods) keep their logs after they exit.

---

## Architecture

```text
   All pod logs
      │  (tailed on every node)
      ▼
   Promtail (DaemonSet)
      │  push
      ▼
   Loki (single binary, filesystem PVC)      namespace: monitoring
      │  query (LogQL)
      ▼
   Grafana  ── Loki data source ── Explore / Logs dashboard
```

Loki and Grafana share the `monitoring` namespace; Grafana reaches Loki via the
in-cluster Service DNS (`http://loki-stack.monitoring.svc.cluster.local:3100`).

---

## Design Decisions

- **Loki + Promtail** (Grafana's own stack): Loki is label-based and Grafana-native,
  so logs land in the existing Grafana next to metrics with no new UI. Promtail is
  the simplest Loki collector.
- **Single binary + filesystem storage** (via the `loki-stack` chart): lowest
  footprint, fine for a learning cluster. Logs live on Loki's PVC and are lost if the
  PVC is deleted. Durable **GCS-backed** storage is deferred to Iteration 2.
- **Grafana data source via the sidecar** (ConfigMap labeled
  `grafana_datasource: "1"`): GitOps-provisioned, consistent with the dashboards.
- **Reused the `monitoring` namespace and the `monitoring-workloads` ArgoCD app** so
  the datasource and logs dashboard deploy with no new plumbing.

---

## Components

- `loki-stack` Helm chart — Loki (single binary) + Promtail (namespace: `monitoring`)
- Grafana Loki data source (`kubernetes/workloads/monitoring/loki-datasource.yaml`)
- Logs dashboard (`kubernetes/workloads/monitoring/loan-api-logs-dashboard.yaml`)
- ArgoCD Applications (`loki-stack`, existing `monitoring-workloads`)

---

## Deployment Flow

1. Check node capacity (Loki single binary + Promtail is light).
2. Install `loki-stack` via ArgoCD (Loki + Promtail; Grafana/Prometheus subcharts
   disabled to avoid duplicates).
3. Add the Loki data source ConfigMap (sidecar-provisioned).
4. Add a logs dashboard (sidecar-provisioned).
5. Verify logs in Grafana Explore / dashboard.

---

## Commands

### Install loki-stack (ArgoCD)

`kubernetes/applications/loki-stack.yaml` — Helm chart `loki-stack` from
`https://grafana.github.io/helm-charts`, key values:

```yaml
loki:
  enabled: true
  persistence:
    enabled: true
    size: 10Gi
promtail:
  enabled: true
grafana:
  enabled: false        # already have Grafana (kube-prometheus-stack)
prometheus:
  enabled: false        # already have Prometheus
```

### Data source (sidecar)

`kubernetes/workloads/monitoring/loki-datasource.yaml` — ConfigMap labeled
`grafana_datasource: "1"` pointing at the **actual Loki service name**:

```yaml
url: http://loki-stack.monitoring.svc.cluster.local:3100
```

### Verify

```bash
kubectl get pods -n monitoring | grep -E 'loki|promtail'   # loki-stack-0 + one promtail per node
kubectl get svc  -n monitoring | grep loki                 # confirm the service name/port (3100)

# readiness + the endpoint Grafana's health check actually uses
kubectl run curltest --image=curlimages/curl -n monitoring --restart=Never -it --rm -- \
  curl -s http://loki-stack.monitoring.svc.cluster.local:3100/ready
kubectl run curltest --image=curlimages/curl -n monitoring --restart=Never -it --rm -- \
  curl -s "http://loki-stack.monitoring.svc.cluster.local:3100/loki/api/v1/labels"
```

### Query logs (Grafana Explore or the logs dashboard)

```logql
{namespace="application"}
{namespace="application", pod=~"loan-api.*"}
{namespace="kubeflow"}
{namespace=~"application|kubeflow|mlflow"} |~ "(?i)error"
```

---

## Expected Outcome

- Loki (`loki-stack-0`) and a Promtail pod per node Running in `monitoring`
- Loki appears as a Grafana data source
- LogQL queries return live pod logs in Grafana Explore and the "Loan API - Logs"
  dashboard

---

## Result

The platform now has centralized logging. Promtail ships every pod's logs to Loki,
and Grafana queries them alongside metrics — giving a single place to correlate a
metrics spike with the underlying log lines. This completes the observability stack
(metrics + logs) and the last functional phase of Iteration 1.

---

## Notes / Lessons Learned

- **`localhost` is not Loki.** Grafana runs in its own pod; the data source URL must
  be the Loki Service DNS (`http://<loki-svc>.monitoring.svc.cluster.local:3100`),
  never `localhost:3100` (which is the Grafana pod itself).
- **Confirm the real service name.** The `loki-stack` release names the Loki service
  `loki-stack` (not `loki`); the data source URL must match exactly.
- **Grafana's "Save & test" is a false negative for Loki.** It probes the labels
  endpoint and often reports "Unable to connect" even when the data source works.
  The real test is running a LogQL query in Explore — if logs return, it is fine.
- **No labels until there are logs.** Immediately after install, Promtail may not
  have shipped anything yet, so `/loki/api/v1/labels` is empty; give it a minute and
  generate some pod activity.
- **Filesystem storage is ephemeral.** Logs live on Loki's PVC; deleting it loses
  them. GCS-backed durable storage is an Iteration 2 upgrade.

---

## Next

- **Iteration 1 is functionally complete** — infra → GitOps → training → registry →
  serving (FastAPI + KServe) → orchestration (Kubeflow) → CI/CD → metrics + logs.
- **Iteration 2 (Hardening):** Workload Identity / OIDC, Secret Manager + External
  Secrets, TLS + domain, network policies, HA, alerting, KServe Serverless, full
  Kubeflow, multi-step pipeline, and **durable GCS-backed Loki storage** +
  Promtail → Grafana Alloy migration.
