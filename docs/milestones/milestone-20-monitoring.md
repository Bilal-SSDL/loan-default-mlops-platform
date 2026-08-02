# Milestone 20 - Monitoring (Prometheus + Grafana)

## Objective

Add observability to the platform with the **kube-prometheus-stack** (Prometheus,
Grafana, Alertmanager, node-exporter, kube-state-metrics). Collect cluster/infra
metrics out of the box, instrument the FastAPI inference service to expose
application metrics, scrape them with a `ServiceMonitor`, and visualize model-serving
request rate, latency, and error rate in a GitOps-provisioned Grafana dashboard.

---

## Architecture

```text
   node-exporter / kube-state-metrics ─┐
                                        ├─► Prometheus ─► Grafana (dashboards)
   loan-api /metrics  ◄── ServiceMonitor┘        │
   (prometheus-fastapi-instrumentator)           └─► Alertmanager (routing: Iteration 2)
```

- **Prometheus** scrapes cluster exporters and the `loan-api` `/metrics` endpoint.
- **Grafana** renders the bundled Kubernetes dashboards plus a custom inference
  dashboard.
- **Alertmanager** is installed but alert rules/routing are deferred to Iteration 2.

---

## Design Decisions

- **kube-prometheus-stack** (not a hand-rolled Prometheus + Grafana): one Helm chart
  brings the Prometheus Operator, Grafana, Alertmanager, and the cluster exporters,
  with ServiceMonitor/PrometheusRule CRDs — the standard, GitOps-friendly choice.
- **Instrument the FastAPI app** with `prometheus-fastapi-instrumentator` to expose
  real inference metrics (request rate, latency, error rate) — not just infra
  health. The KServe path reuses the same image, so it is covered too.
- **Dashboard provisioned as a ConfigMap** (Grafana sidecar) so it is version
  controlled and survives Grafana pod restarts — consistent with the rest of the
  GitOps setup.
- **Alerting deferred to Iteration 2.** Alertmanager is running; PrometheusRule
  alerts and receiver routing (Slack/email) are an Iteration 2 item.

---

## Components

- `kube-prometheus-stack` Helm chart (namespace: `monitoring`)
- FastAPI `/metrics` endpoint (`prometheus-fastapi-instrumentator`)
- `ServiceMonitor` (`kubernetes/workloads/serving/servicemonitor.yaml`)
- Grafana dashboard ConfigMap (`kubernetes/workloads/monitoring/loan-api-dashboard.yaml`)
- ArgoCD Applications (`kube-prometheus-stack`, `monitoring-workloads`)

---

## Deployment Flow

1. Check node capacity (Prometheus is memory-hungry).
2. Install kube-prometheus-stack via ArgoCD.
3. Instrument the FastAPI app; CI/CD rebuilds and deploys `loan-api`.
4. Add a `ServiceMonitor` so Prometheus scrapes `/metrics`.
5. Provision the inference dashboard as a sidecar ConfigMap.
6. Generate traffic and verify metrics/dashboard.

---

## Commands

### Install kube-prometheus-stack (ArgoCD)

ArgoCD Application `kubernetes/applications/kube-prometheus-stack.yaml` (Helm), key
values:

```yaml
prometheus:
  prometheusSpec:
    serviceMonitorSelectorNilUsesHelmValues: false   # scrape ServiceMonitors from any namespace
    ruleSelectorNilUsesHelmValues: false
```

`ServerSideApply=true` is required (the stack's CRDs are large).

### Instrument the FastAPI app

`ml/requirements.txt`:

```
prometheus-fastapi-instrumentator==7.0.0
```

`ml/api/main.py` (after `app = FastAPI(...)`):

```python
from prometheus_fastapi_instrumentator import Instrumentator

# Exposes GET /metrics with request count, latency histograms, and status codes.
Instrumentator().instrument(app).expose(app)
```

Commit + push -> CI/CD rebuilds `loan-api`, writes back the tag, ArgoCD rolls it out.

### ServiceMonitor

`kubernetes/workloads/serving/servicemonitor.yaml` selects the `loan-api` Service and
scrapes its named `http` port at `/metrics`. The Service port must be **named**
(`name: http`) for the ServiceMonitor `endpoints.port: http` to match.

### Provision the dashboard (GitOps)

`kubernetes/workloads/monitoring/loan-api-dashboard.yaml` is a ConfigMap labeled
`grafana_dashboard: "1"` containing the dashboard in the **classic Grafana JSON
model** (not the newer `dashboard.grafana.app/v2` export format, which the sidecar
does not load). Deployed by the `monitoring-workloads` ArgoCD Application.

### Access Grafana / Prometheus

```bash
kubectl port-forward svc/kube-prometheus-stack-grafana -n monitoring 3000:80
# http://127.0.0.1:3000   user: admin   pass: prom-operator (or the value set in Helm)

kubectl port-forward svc/kube-prometheus-stack-prometheus -n monitoring 9090:9090
# http://127.0.0.1:9090/targets   -> loan-api target should be UP
```

### Verify + generate traffic

```bash
# confirm the app exposes metrics
kubectl port-forward svc/loan-api -n application 8000:8000
curl -s http://127.0.0.1:8000/metrics | grep http_requests_total

# generate /predict traffic so the per-route series exist
for i in $(seq 1 60); do
  curl -s -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" \
    -d '{ "year":2019,"loan_limit":"cf","Gender":"Sex Not Available","approv_in_adv":"nopre","loan_type":"type1","loan_purpose":"p1","Credit_Worthiness":"l1","open_credit":"nopc","business_or_commercial":"nob/c","loan_amount":116500,"term":360.0,"Neg_ammortization":"not_neg","interest_only":"not_int","lump_sum_payment":"not_lpsm","construction_type":"sb","occupancy_type":"pr","Secured_by":"home","total_units":"1U","income":1740.0,"credit_type":"EXP","Credit_Score":758,"co-applicant_credit_type":"CIB","age":"25-34","submission_of_application":"to_inst","Region":"south","Security_Type":"direct" }' > /dev/null
  sleep 1
done
```

---

## Dashboard Queries

Panels use `$__rate_interval` (adapts to the scrape interval) rather than a hardcoded
`[5m]`:

- **Request rate (/predict):**
  `sum(rate(http_requests_total{handler="/predict"}[$__rate_interval]))`
- **p95 latency (/predict):**
  `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{handler="/predict"}[$__rate_interval])) by (le))`
- **5xx error rate (/predict):**
  `sum(rate(http_requests_total{status="5xx",handler="/predict"}[$__rate_interval]))`

---

## Expected Outcome

- kube-prometheus-stack pods Running in `monitoring`
- `loan-api` scrape target UP in Prometheus (`/targets`)
- `/metrics` exposes `http_requests_total`, `http_request_duration_seconds_*`
- Grafana shows the bundled Kubernetes dashboards + the "Loan API - Inference"
  dashboard, populated once `/predict` traffic exists

---

## Result

The platform now has metrics-based observability. Cluster and pod health come from
the bundled exporters, and the FastAPI/KServe serving path exposes request, latency,
and error metrics that Prometheus scrapes and Grafana visualizes. The inference
dashboard is provisioned via GitOps and survives restarts.

---

## Notes / Lessons Learned

- **`serviceMonitorSelectorNilUsesHelmValues: false` is essential.** Without it,
  Prometheus only scrapes ServiceMonitors carrying the chart's release label and
  silently ignores yours — the #1 cause of a target never appearing.
- **Named Service port.** The ServiceMonitor `endpoints.port` matches the Service
  port **name** (`http`), not the number.
- **No data until there is traffic.** A per-route counter like
  `http_requests_total{handler="/predict"}` does not exist until `/predict` is
  called, and `rate(...)` needs recent samples — generate traffic and view a short
  time range (Last 5-15 min).
- **Grouped status codes.** The instrumentator groups status codes by default, so
  the label value is `status="5xx"` (not `"500"`); filter with `status="5xx"`, not
  `status=~"5.."`.
- **Dashboard export format.** Grafana v13 exports the new
  `dashboard.grafana.app/v2` schema, which the sidecar cannot provision. The
  ConfigMap must contain the **classic dashboard JSON model** (top-level `panels`,
  `schemaVersion`, `templating`).
- **PromQL is not the place for display units.** Panel unit (reqps, seconds) is set
  in the panel's Standard options, not appended to the query — appending
  `(unit: req/s)` causes a `parse error: unexpected "("`.
- **App instrumentation flows through CI/CD.** The `ml/api` + `requirements.txt`
  change tripped the `api` path filter, so CI rebuilt and ArgoCD deployed `loan-api`
  automatically — no manual image build.

---

## Next

- **Phase 8 - Logging:** Loki + Fluent Bit for centralized log aggregation,
  queryable alongside metrics in Grafana.
- **Iteration 2:** alerting (PrometheusRule rules + Alertmanager receiver routing to
  Slack/email); dashboards for MLflow/Kubeflow; a second ServiceMonitor for the
  KServe `loan-default-predictor`.
