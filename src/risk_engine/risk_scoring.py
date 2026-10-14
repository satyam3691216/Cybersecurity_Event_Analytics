"""
Rule-based risk scoring for cybersecurity events.
"""

import pandas as pd


def calculate_risk_score(
    failed_logins: int = 0,
    new_ip: bool = False,
    new_device: bool = False,
) -> int:
    """
    Calculate a risk score using configurable detection rules.

    Rules:
    - Failed login: +10 points
    - Five or more failed logins: +40 points
    - New IP address: +20 points
    - New device: +20 points

    The final score is capped at 100.
    """

    score = 0

    if failed_logins > 0:
        score += 10

    if failed_logins >= 5:
        score += 40

    if new_ip:
        score += 20

    if new_device:
        score += 20

    return min(score, 100)


def get_risk_level(score: int) -> str:
    """Classify a numeric risk score."""

    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"