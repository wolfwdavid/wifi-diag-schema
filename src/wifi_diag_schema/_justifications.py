"""Per-field 'why-allowlisted' justifications (D-01 privacy contract).

The schema source IS the privacy policy. Each extended field documents its
OS-source + confidence per platform so reviewers can audit the privacy lens.

When you add a field to TelemetryFrame, you MUST also add a constant here
documenting why the field is allowlisted (Pitfall 1).
"""
from __future__ import annotations

PER_PACKET_RETRY_COUNT = (
    "why-allowlisted: high retry rate is a key sticky-client / RF-interference "
    "signature. Sources by OS: Linux iw (HIGH), macOS CoreWLAN txRetries (MEDIUM, "
    "may require entitlements), Windows Native Wifi WLAN_STATISTICS.MACUcastCounters.Retries "
    "(MEDIUM, NDIS-level). None when not collected; classifier handles absence as a feature."
)

RTS_CTS_RATE = (
    "why-allowlisted: hidden-node / contention indicator. Linux iw HIGH; "
    "None elsewhere (Phase 4 may add Windows path, additive minor bump per D-05)."
)

BEACON_RSSI_DBM = (
    "why-allowlisted: beacon RSSI vs data-frame RSSI delta detects driver / "
    "power-save anomalies. Linux iw HIGH; Windows netsh wlan show MEDIUM; macOS CoreWLAN MEDIUM."
)

NEIGHBOR_AP_COUNT_5GHZ = (
    "why-allowlisted: high count + low RSSI = sticky-client signature. "
    "All OSes via passive scan; LOW-MEDIUM availability without active scan."
)

BSSID = (
    "why-allowlisted: AP identity. Two modes (D-03): raw MAC (opt-in flag, "
    "default OFF, unlocks vendor-aware diagnosis via OUI) or per-session SHA-256 hash "
    "(default). Validator accepts either format string. The `bssid_mode` sibling "
    "field disambiguates which format is in use (RESEARCH Open Question 2)."
)
