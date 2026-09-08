# Kubernetes monitoring

Prometheus (metrics) + VictoriaLogs (logs) + Grafana. Namespace: `monitoring`.

## Flow

```
Cluster
  ├── nodes ──► node-exporter ─────────────┐
  ├── apps / API ──► kube-state-metrics ───┼──► Prometheus ──► Grafana (metrics)
  └── container logs ──► vlagent ──► VictoriaLogs ──► Grafana (logs)
```

Metrics are pulled by Prometheus. Logs are pushed by vlagent into VictoriaLogs. Grafana reads both.

## Components

| Component | Role |
| --- | --- |
| Prometheus | Stores metrics |
| node-exporter | Node CPU, RAM, disk, network |
| kube-state-metrics | App/pod state, CPU/memory requests and limits |
| VictoriaLogs | Stores logs |
| vlagent | Collects container logs on every node |
| Grafana | Dashboards and Explore |

## Prerequisites

- `kubectl` and a cluster

## Install

```bash
kubectl apply -k k8s-monitoring
kubectl -n monitoring get pods -w
```

Wait until all pods are `Running`.

## Open Grafana

```bash
kubectl -n monitoring port-forward svc/grafana 3000:3000
```

Open http://localhost:3000 — user `admin`, password `admin`.

Datasources **Prometheus** and **VictoriaLogs** are already provisioned.

Optional:

```bash
kubectl -n monitoring port-forward svc/prometheus 9090:9090
kubectl -n monitoring port-forward svc/victoria-logs 9428:9428
```

- Prometheus UI: http://localhost:9090
- VictoriaLogs UI: http://localhost:9428/select/vmui/

## What is collected

| Source | What you get |
| --- | --- |
| node-exporter | Node CPU, RAM, disk, network |
| kube-state-metrics | App/pod state, CPU/memory requests and limits |
| vlagent → VictoriaLogs | Container logs from every node |

Logs: Explore → VictoriaLogs, e.g. `kubernetes.pod_namespace:monitoring`

## Uninstall

```bash
kubectl delete -k k8s-monitoring
```
