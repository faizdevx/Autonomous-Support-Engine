from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SOPDefinition:
    sop_id: str
    label: str
    category: str
    intent_keywords: tuple[str, ...]
    required_data: tuple[str, ...]
    steps: tuple[str, ...]
    escalation_conditions: tuple[str, ...]
    resolution_template: str
    missing_context_template: str


SOP_REGISTRY: dict[str, SOPDefinition] = {
    "refund_not_received": SOPDefinition(
        sop_id="refund_not_received",
        label="Refund Not Received",
        category="billing",
        intent_keywords=("refund", "money back", "charged twice", "food was bad", "order issue"),
        required_data=("order_id", "refund_request_date", "payment_method"),
        steps=(
            "Validate the issue is about a refund or post-purchase dissatisfaction.",
            "Retrieve billing refund context from the knowledge base.",
            "Respond only with verified refund timing or next steps from retrieved context.",
            "Escalate if the refund window, refund status, or identity checks are missing.",
        ),
        escalation_conditions=(
            "No refund-related knowledge chunks were retrieved.",
            "The customer asks for a policy exception not covered in context.",
            "Required order or payment details are missing.",
        ),
        resolution_template=(
            "I checked the refund support guidance for your case. Based on the available context: "
            "{context_summary} Please reply with your order ID, refund request date, and payment method "
            "if you want us to verify the refund timeline."
        ),
        missing_context_template=(
            "I do not have enough verified refund context to answer this safely. "
            "Please share your order ID, refund request date, and payment method so we can escalate it."
        ),
    ),
    "login_issue": SOPDefinition(
        sop_id="login_issue",
        label="Login Issue",
        category="login",
        intent_keywords=("login", "otp", "password", "account locked", "sign in"),
        required_data=("email", "last_login_attempt_at", "device_or_browser"),
        steps=(
            "Validate the issue is authentication related.",
            "Retrieve login troubleshooting context from the knowledge base.",
            "Respond only with the retrieval-backed recovery actions.",
            "Escalate if account state, OTP delivery, or recovery steps are not grounded in context.",
        ),
        escalation_conditions=(
            "No login-related knowledge chunks were retrieved.",
            "The customer reports a security lockout or repeated OTP failure without context support.",
            "Required account details are missing.",
        ),
        resolution_template=(
            "I checked the login support guidance for your case. Based on the available context: "
            "{context_summary} Please reply with your email, approximate time of the last login attempt, "
            "and device or browser if you want us to verify the login path."
        ),
        missing_context_template=(
            "I do not have enough verified login context to answer this safely. "
            "Please share your email, last login attempt time, and device or browser so we can escalate it."
        ),
    ),
}


def match_sop(user_input: str) -> SOPDefinition | None:
    text = user_input.lower()
    for sop in SOP_REGISTRY.values():
        if any(keyword in text for keyword in sop.intent_keywords):
            return sop
    return None
