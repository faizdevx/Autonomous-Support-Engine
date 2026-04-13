"""Context retrieval and policy helpers for knowledge agents."""

from typing import Dict


def fetch_user_data(customer_id: str) -> Dict[str, str]:
    return {"account_status": "active"}


def check_order_status(order_id: str) -> Dict[str, str]:
    return {"status": "processed", "date": "April 7"}


def retrieve_policy(issue: str) -> str:
    if issue == "refund":
        return "Refund takes 7-10 days"
    return "No policy available for this request"
