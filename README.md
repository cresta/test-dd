[![Docker Repository on Quay](https://quay.io/repository/cresta/test-dd/status "Docker Repository on Quay")](https://quay.io/repository/cresta/test-dd)
# test-dd
Pod to deploy to verify datadog custom metrics and APM are working

# Usage

You can deploy this container to your k8s cluster to verify both
dogstatsd and APM are working correctly.  Simple pod uses unix
domain sockets to send dogstatsd and APM between two containers.

```
    kubectl apply -f pod.yaml
```
