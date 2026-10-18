# Centralized Logging for 100+ Microservices

```mermaid
flowchart TD
    subgraph K8s["☸ Kubernetes — 100+ Services"]
        S1["Service 1\nconsole.log({ level: 'error', ... })\n→ stdout JSON"]
        S2["Service 2"]
        S3["Service 3"]
        S4["Service 4"]
        SN["+ 96 more..."]
        APPLOG["📄 App Log\n/var/log/pods/..\non every node"]
        S1 --> APPLOG
    end

    APPLOG --> FB["🐦 Fluent Bit\nDaemonSet · SMB RAM · batches"]

    FB --> KF["⚙ Kafka\nshock absorber · absorbs bursts"]

    KF --> LV["🔧 Logstash / Vector\nparse + enrich · tag errors"]

    LV --> ES
    LV --> S3B

    subgraph Storage["Storage Tier"]
        ES["🔍 Elasticsearch\n7 days · ms fast · hot tier · on-call lives"]
        S3B["🪣 S3\ncold logs · 1 year · cheap"]
    end

    ES --> KIB["📊 Kibana\nengineers search"]
    ES --> EA["🚨 ElastAlert\nfires on errors"]
```

## Pipeline Summary

| Stage | Tool | Role |
|---|---|---|
| **Collection** | Fluent Bit (DaemonSet) | Tails `/var/log/pods` on every node, low memory |
| **Buffering** | Kafka | Shock absorber — decouples producers from consumers |
| **Processing** | Logstash / Vector | Parses, enriches, and tags log severity |
| **Hot Storage** | Elasticsearch | 7-day retention, millisecond queries for on-call engineers |
| **Cold Storage** | S3 | 1-year retention, cheap archival |
| **Visualization** | Kibana | Engineers search and explore logs |
| **Alerting** | ElastAlert | Fires alerts on error patterns |
