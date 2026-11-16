# payments-worker: Kafka consumer lag

## When this applies
The alert PaymentsLagHigh fires when the consumer group `payments-worker` is more than 10,000 messages behind on the topic `payments.events`.

## Check
1. Count the workers: `kubectl -n payments get deploy payments-worker`.
2. The topic has 12 partitions, so more than 12 workers do not help: the extra ones sit idle.

## Fix
- Fewer than 12 workers: scale up with `kubectl -n payments scale deploy/payments-worker --replicas=12`.
- Already 12: one slow message blocks its partition; find it on the Grafana board "Payments / Kafka", panel "Oldest message per partition".
