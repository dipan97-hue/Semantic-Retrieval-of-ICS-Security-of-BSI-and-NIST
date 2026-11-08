
# Attack potential factor values

ELAPSED_TIME = {
    "<=1 day": 0,
    "<=1 week": 1,
    "<=1 month": 4,
    "<=6 months": 17,
    ">6 months": 19
}

SPECIALIST_EXPERTISE = {
    "Layman": 0,
    "Proficient": 3,
    "Expert": 6,
    "Multiple experts": 8
}

KNOWLEDGE = {
    "Public": 0,
    "Restricted": 3,
    "Confidential": 7,
    "Strictly confidential": 11
}

WINDOW_OF_OPPORTUNITY = {
    "Unlimited": 0,
    "Easy": 1,
    "Moderate": 4,
    "Difficult/none": 10
}

EQUIPMENT = {
    "Standard": 0,
    "Specialized": 4,
    "Bespoke": 7,
    "Multiple bespoke": 9
}


# Defined risk matrix

RISK_MATRIX = {
    "Severe": {
        "Very Low": 2,
        "Low": 3,
        "Medium": 4,
        "High": 5
    },
    "Major": {
        "Very Low": 1,
        "Low": 2,
        "Medium": 3,
        "High": 4
    },
    "Moderate": {
        "Very Low": 1,
        "Low": 2,
        "Medium": 2,
        "High": 3
    },
    "Negligible": {
        "Very Low": 1,
        "Low": 1,
        "Medium": 1,
        "High": 1
    }
}


def calculate_attack_potential(step):
    """Calculate APS for one attack-path step."""

    try:
        values = [
            ELAPSED_TIME[step["elapsed_time"]],
            SPECIALIST_EXPERTISE[step["specialist_expertise"]],
            KNOWLEDGE[step["knowledge_of_item"]],
            WINDOW_OF_OPPORTUNITY[step["window_of_opportunity"]],
            EQUIPMENT[step["equipment"]]
        ]
    except KeyError as exc:
        raise ValueError(
            f"Missing or invalid attack potential factor: {exc}"
        )

    return sum(values)


def calculate_attack_feasibility(attack_potentials):
    """Calculate arithmetic mean of step APS values."""

    if not attack_potentials:
        raise ValueError("At least one attack-path step is required.")

    return sum(attack_potentials) / len(attack_potentials)


def get_feasibility_rating(afv):
    """Convert AFV into the defined feasibility rating."""

    if afv < 0:
        raise ValueError("Invalid attack feasibility value.")

    if afv < 14:
        return "High"

    elif afv < 20:
        return "Medium"

    elif afv < 25:
        return "Low"

    return "Very Low"


def calculate_risk(impact_rating, feasibility_rating):
    """Calculate risk using the defined risk matrix."""

    if impact_rating not in RISK_MATRIX:
        raise ValueError("Invalid impact rating.")

    if feasibility_rating not in RISK_MATRIX[impact_rating]:
        raise ValueError("Invalid feasibility rating.")

    return RISK_MATRIX[impact_rating][feasibility_rating]


def assess_attack_path(steps):
    """Calculate APS for every step and AFV/rating for the path."""

    if not steps:
        raise ValueError("Attack path must contain at least one step.")

    step_results = []

    for step in steps:
        aps = calculate_attack_potential(step)

        step_results.append({
            "step_id": step.get("id"),
            "description": step.get("description"),
            "attack_potential": aps
        })

    afv = calculate_attack_feasibility(
        [item["attack_potential"] for item in step_results]
    )

    return {
        "steps": step_results,
        "attack_feasibility_value": round(afv, 2),
        "attack_feasibility_rating": get_feasibility_rating(afv)
    }
