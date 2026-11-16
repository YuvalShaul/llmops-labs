# Node: disk almost full

## When this applies
The alert NodeDiskPressure fires when a node's root disk is over 85% full.

## Check
1. Find the node: `kubectl get nodes`, and look for the condition DiskPressure.
2. On our clusters the usual cause is old container images: the image garbage collection starts only at 90%.

## Fix
- Cordon the node first: `kubectl cordon <node>`, so no new pods land on it.
- Our nodes are replaced, never cleaned by hand: drain it with `kubectl drain <node> --ignore-daemonsets`, and the autoscaler starts a new node.
