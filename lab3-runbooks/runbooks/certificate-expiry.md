# Ingress: certificate about to expire

## When this applies
The alert CertExpiresSoon fires 14 days before a TLS certificate of one of our ingresses expires.

## Check
1. Our certificates are issued by cert-manager: `kubectl -n <namespace> get certificate`.
2. A certificate that does not renew shows READY False; read why with `kubectl -n <namespace> describe certificate <name>`.

## Fix
- The usual cause is the DNS challenge: the cert-manager role lost its permission on the DNS zone `payments.example.internal`.
- Open a ticket for the platform team; they own that role.
