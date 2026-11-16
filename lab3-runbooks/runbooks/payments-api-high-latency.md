# payments-api: high latency

## When this applies
The alert PaymentsApiSlow fires when the p95 response time of payments-api is over 800 ms for 5 minutes.

## Check
1. Look at the database connection pool first: `kubectl -n payments exec deploy/payments-api -- curl -s localhost:8080/metrics | grep db_pool_in_use`.
2. If `db_pool_in_use` equals `db_pool_size`, the pool is exhausted: every request waits for a connection.
3. Otherwise check the latency of the ledger service on the Grafana board "Payments / Dependencies".

## Fix
- An exhausted pool: raise `POOL_SIZE` in the ConfigMap `payments-db` from 20 to 40, then run `kubectl -n payments rollout restart deploy/payments-api`.
- Never raise it above 60: the database allows 200 connections, shared by three services.
- A slow ledger service: page the ledger team in #ledger-oncall.
