# data_stack

Pet-project Data Stack with GitOps on Argo CD (App of Apps pattern).

## Target architecture

- Argo CD deploys all components via GitOps.
- Airflow orchestrates data jobs (future DAGs can read from Kafka or trigger processing).
- Kafka is an event/log backbone.
- `log-producer` service generates logs/events to Kafka.
- `log-consumer` service reads logs/events from Kafka.
- Separate `dev` and `prod` environments with isolated values and scaling.

## Recommended interaction model (best practice)

1. **Producer -> Kafka topic** (`app-logs`) for raw event ingestion.
2. **Consumer <- Kafka topic** for downstream processing or persistence.
3. **Airflow** does not sit in the hot path for every event; it orchestrates:
   - batch enrich/aggregate jobs,
   - periodic replay/backfill from Kafka,
   - monitoring workflows and alerting DAGs.
4. **GitOps flow**:
   - commit change to repo,
   - Argo CD syncs environment,
   - workloads are reconciled automatically.

This keeps real-time flow in Kafka services, while Airflow remains an orchestrator.

## Repository layout

- `argocd/`:
  - `projects/`: Argo CD `AppProject`.
  - `root-apps/`: App of Apps root `Application` for `dev` and `prod`.
  - `environments/`: environment composition only (`kustomization.yaml` that selects component overlays).
  - `apps/`: component-first Argo definitions (`base + overlays + values`) for Airflow, Kafka and custom services.
- `apps/`: Kubernetes manifests (Kustomize) for custom services (`log-producer`, `log-consumer`).
- `services/`: Python source code for producer/consumer (one folder per service, one `pyproject.toml` per service).
- `infra/terraform/`: placeholder for future EKS Terraform.

## Versions pinned from upstream repos

- **Apache Airflow**: `3.2.0` (from apache/airflow releases).
- **Apache Kafka**: `4.2.0` (from apache/kafka tags/releases stream).
- **Airflow Helm chart**: `1.20.0`.
- **Bitnami Kafka Helm chart**: `32.4.3`.

## `uv` environment strategy

Use **separate `uv` environment per service** (already scaffolded):

- `services/log-producer`
- `services/log-consumer`

Why:

- isolated dependencies and safer upgrades;
- independent image build/deploy lifecycle;
- closer to real microservice operations.

## What to do next

1. Replace placeholder repo URL `https://github.com/your-org/data_stack.git` in `argocd/` manifests.
2. Build/push container images for both services and set immutable tags instead of `latest`.
3. Add Secrets management (SOPS/External Secrets) for sensitive env vars.
4. Add namespace/network policies and resource requests/limits.
5. Add Terraform EKS module and Argo CD bootstrap module in `infra/terraform`.