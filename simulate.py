import time
import random
import csv
import sys
from unittest.mock import patch

# Mock LLM before importing
# Global counter for forcing bad drafts
call_count = 0

def mock_call_llm(prompt):
    global call_count
    call_count += 1

    if "Classify into:" in prompt:
        if "refund" in prompt.lower():
            return "billing_refund"
        elif "login" in prompt.lower() or "otp" in prompt.lower():
            return "auth_login"
        else:
            return "billing_refund"  # default
    elif "Use ONLY the provided context" in prompt:
        if "improve" in prompt.lower():
            return "I understand your concern. Your refund was processed and will arrive in 7-10 days. Please wait 2-3 more days."
        else:
            # Force bad drafts for first few calls
            if call_count % 10 < 3:  # Every 10 calls, first 3 are bad
                return "Your refund is processed. Wait."
            else:
                return "I understand your concern. Your refund was processed and will arrive in 7-10 days. Please wait 2-3 more days."
    else:
        return "billing_refund"

with patch.dict('sys.modules', {'llm.hf_model': type(sys)('llm.hf_model')}):
    sys.modules['llm.hf_model'].call_llm = mock_call_llm

    from services.ticket_processor import process_ticket
    from models.state import TicketState

    # Sample queries (based on your dataset categories)
    QUERIES = [
        "My refund not processed",
        "I am charged twice",
        "Login OTP not received",
        "Account locked issue",
        "API not responding",
    ]

    def simulate(n=50):
        results = []

        for i in range(n):
            query = random.choice(QUERIES)

            state = TicketState(
                ticket_id=f"TCK-{i:03d}",
                user_input=query
            )

            start = time.time()

            final_state = process_ticket(state)

            latency = time.time() - start

            results.append({
                "ticket_id": state.ticket_id,
                "status": final_state.status,
                "latency": round(latency, 2),
                "revisions": final_state.revision_count,
                "confidence": final_state.confidence_score or 0.0,
                "improved": final_state.revision_count > 0,
                "drafts": final_state.drafts,
                "critic_history": final_state.critic_history
            })

        return results


    def compute_metrics(results):
        total = len(results)

        resolved = sum(1 for r in results if r["status"] == "Auto-Resolved")
        escalated = sum(1 for r in results if r["status"] == "Escalated")

        avg_latency = sum(r["latency"] for r in results) / total

        return {
            "resolution_rate": resolved / total,
            "escalation_rate": escalated / total,
            "avg_latency": avg_latency
        }


    def save_csv(results):
        with open("metrics.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)


    if __name__ == "__main__":
        data = simulate(50)
        save_csv(data)

        metrics = compute_metrics(data)
        print("Simulation complete → metrics.csv generated")
        print(f"Metrics: {metrics}")