# Fit profile schema

Record values in MiB and GiB as indicated. Use `null` for unmeasured values; never substitute zero.

```json
{
  "server": {
    "vcpu": 2,
    "ram_mib": 2048,
    "swap_mib": 0,
    "disk_free_gib": 30
  },
  "reserved": {
    "os_and_services_mib": 512,
    "disk_safety_gib": 5
  },
  "application": {
    "steady_rss_mib": null,
    "peak_runtime_mib": null,
    "peak_build_mib": null,
    "installed_disk_gib": null,
    "release_and_rollback_gib": null
  },
  "plan": {
    "build_on_server": false,
    "memory_headroom_percent": 25
  }
}
```

Measure application RSS under a representative flow, not only at idle. Include at least the intended number of workers. `release_and_rollback_gib` must retain the active version, one rollback version, and temporary extraction space.
