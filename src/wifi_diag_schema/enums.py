"""Literal type aliases for all enum-shaped fields.

Per CONTEXT D-Discretion + RESEARCH Pattern 2: Literal over Enum gives cleaner
JSON Schema for Anthropic Structured Outputs (just an `enum` array, no $defs
indirection).
"""
from __future__ import annotations

from typing import Literal

OS = Literal["windows", "macos", "linux"]
NetworkMode = Literal["enterprise", "captive", "home", "unknown"]
AuthEventClass = Literal[
    "none",
    "8021x_success",
    "8021x_fail",
    "radius_timeout",
    "eap_fail",
    "eapol_m3_timeout",
]
DhcpEventClass = Literal[
    "none",
    "discover_no_offer",
    "nak_on_renew",
    "request_loop",
]
DriverState = Literal[
    "normal",
    "post_wake_init",
    "power_save_active",
    "u_apsd_active",
    "error",
    "unknown",
]
MacRandomizationState = Literal[
    "off",
    "per_network",
    "per_session",
    "rejected",
]
BssidMode = Literal["raw", "hashed"]  # disambiguates bssid format (D-03 + RESEARCH Open Question 2)

# Class slugs for Verdict.top_class — must match model/synth/state_machines/{slug}.py
DisconnectClass = Literal[
    "auth_8021x_eap_fail",
    "ap_roam_rekey_fail",
    "radius_timeout",
    "captive_portal_expiry",
    "mac_randomization_reject",
    "dhcp_lease_churn",
    "dns_resolver_fail",
    "driver_power_save_wake",
    "rf_sticky_client",
    "isp_upstream_fail",
]

# Phase 3 D-VERDICT-05: plain-English display labels for the verdict UI.
# Both the LLM narrator and the templated/no-LLM narrator (Phase 4 local-only
# mode) read this dict so the rendered class label is identical regardless of
# which path produced the Verdict. Insertion order mirrors the canonical
# DisconnectClass Literal above (test_display_names_keys_match_canonical_order).
DISPLAY_NAMES: dict[DisconnectClass, str] = {
    "auth_8021x_eap_fail": "802.1X authentication failure",
    "ap_roam_rekey_fail": "Access-point roam re-key failure",
    "radius_timeout": "RADIUS server timeout",
    "captive_portal_expiry": "Captive portal session expired",
    "mac_randomization_reject": "MAC randomization rejected",
    "dhcp_lease_churn": "DHCP lease churn",
    "dns_resolver_fail": "DNS resolver failure",
    "driver_power_save_wake": "Wi-Fi driver power-save wake bug",
    "rf_sticky_client": "Sticky client on weak access point",
    "isp_upstream_fail": "Upstream ISP failure",
}
