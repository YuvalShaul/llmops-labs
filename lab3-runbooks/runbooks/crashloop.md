# Any pod: CrashLoopBackOff

## When this applies
A pod restarts again and again, and its status shows CrashLoopBackOff.

## Check
1. Read the logs of the previous run, not the current one: `kubectl -n <namespace> logs <pod> --previous`.
2. Read the last state of the container: `kubectl -n <namespace> describe pod <pod>`, under "Last State".
3. Exit code 137 means the container was killed for using too much memory (OOMKilled).

## Fix
- OOMKilled: our memory limits live in the Helm chart `platform/charts/<service>/values.yaml`, under `resources.limits.memory`; raise it in a pull request, never with `kubectl edit`.
- A missing secret or variable: check the ExternalSecret of the service, `kubectl -n <namespace> get externalsecret`.
