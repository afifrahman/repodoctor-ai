# Sample target file simulating a failing CI pipeline in a repo
def calculate_user_metrics(events: list) -> dict:
    """Return aggregated metrics for a list of event dicts.

    Each event may be missing 'score' or 'is_active', and 'score' may be None.
    An empty events list is handled gracefully (average defaults to 0).
    """
    total_score = 0
    active_count = 0

    for event in events:
        # FIX 1: Use .get() with a default of 0 so missing or None scores are skipped safely.
        score = event.get("score") or 0
        total_score += score

        # FIX 2: Use .get() with a default of False so a missing 'is_active' key is treated as inactive.
        if event.get("is_active", False):
            active_count += 1

    # FIX 3: Guard against ZeroDivisionError when events is empty.
    average = total_score / len(events) if events else 0

    return {
        "total": total_score,
        "average": average,
        "active_users": active_count
    }

if __name__ == "__main__":
    # Original CI payload that was crashing (score=None is now handled).
    test_payload = [{"score": 10, "is_active": True}, {"score": None, "is_active": False}]
    print(calculate_user_metrics(test_payload))

    # Additional edge-case smoke tests.
    print(calculate_user_metrics([]))                                        # empty list
    print(calculate_user_metrics([{"is_active": True}]))                    # missing 'score' key
    print(calculate_user_metrics([{"score": 5}]))                           # missing 'is_active' key