
def segment_customer(customer):
    interests = customer.get("interests", "").lower()

    if "fitness" in interests:
        return "Fitness Enthusiast"
    elif "fashion" in interests:
        return "Fashion Lover"
    elif "tech" in interests:
        return "Tech Savvy"
    else:
        return "General Audience"
