import random
from database.db import get_connection
from agents.segmentation import segment_customer
from agents.subject_agent import generate_subject
from agents.copywriter import generate_email_body
from agents.evaluator import evaluate_email
from agents.variant_agent import decide_variant_with_reason


def get_variant_stats(campaign_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT variant,
               COUNT(*) AS total_sent,
               AVG(opened) AS open_rate,
               AVG(clicked) AS click_rate,
               AVG(score) AS avg_score
        FROM email_logs
        WHERE campaign_id = %s
        GROUP BY variant
    """, (campaign_id,))

    stats = cursor.fetchall()
    conn.close()
    return stats


def generate_email(customer_id, campaign_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------------- FETCH DATA ----------------
    cursor.execute("SELECT * FROM customers WHERE id=%s", (customer_id,))
    customer = cursor.fetchone()

    cursor.execute("SELECT * FROM campaigns WHERE id=%s", (campaign_id,))
    campaign = dict(cursor.fetchone())

    # ---------------- SEGMENTATION ----------------
    segment = segment_customer(customer)

    variants = []

    # ---------------- GENERATE BOTH VARIANTS ----------------
    for variant in ["A", "B"]:
        campaign["tone"] = "friendly" if variant == "A" else "persuasive"

        subject = generate_subject(customer, campaign)
        body = generate_email_body(customer, campaign)
        score = evaluate_email(subject, body)

        # Open-rate simulation
        opened = random.random() < min(score, 0.95)

        cursor.execute("""
            INSERT INTO email_logs
            (customer_id, campaign_id, subject, body, score, sent_status, variant, opened)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            customer_id,
            campaign_id,
            subject,
            body,
            score,
            "draft",
            variant,
            opened
        ))

        log_id = cursor.lastrowid

        variants.append({
            "variant": variant,
            "segment": segment,
            "subject": subject,
            "body": body,
            "score": score,
            "log_id": log_id,
            "opened": opened
        })

    conn.commit()

    # ---------------- AGENTIC DECISION ----------------
    stats = get_variant_stats(campaign_id)

    if stats and len(stats) >= 2:
        selected_variant, reason = decide_variant_with_reason(stats)
    else:
        selected_variant = "A"
        reason = "Cold start: insufficient historical data"

    conn.close()

    # ---------------- FINAL RESPONSE ----------------
    return {
        "selected_variant": selected_variant,
        "reason": reason,
        "variants": variants
    }



