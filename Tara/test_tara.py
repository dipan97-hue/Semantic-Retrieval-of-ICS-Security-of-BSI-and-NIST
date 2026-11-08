
from Tara.scoring import assess_attack_path, calculate_risk
from Tara.validation import validate_attack_path


steps = [
    {
        "id": "APS-01",
        "description": "Obtain shared PLC credentials",
        "elapsed_time": "<=1 month",
        "specialist_expertise": "Expert",
        "knowledge_of_item": "Restricted",
        "window_of_opportunity": "Moderate",
        "equipment": "Standard"
    },
    {
        "id": "APS-02",
        "description": "Access the PLC programming interface",
        "elapsed_time": "<=1 day",
        "specialist_expertise": "Proficient",
        "knowledge_of_item": "Restricted",
        "window_of_opportunity": "Easy",
        "equipment": "Standard"
    },
    {
        "id": "APS-03",
        "description": "Modify PLC logic",
        "elapsed_time": "<=1 week",
        "specialist_expertise": "Expert",
        "knowledge_of_item": "Confidential",
        "window_of_opportunity": "Moderate",
        "equipment": "Specialized"
    }
]


# 1. Validate the attack path
errors = validate_attack_path(steps)

if errors:
    print("Validation errors:")
    for error in errors:
        print("-", error)

else:
    # 2. Calculate attack feasibility
    result = assess_attack_path(steps)

    print("\nATTACK PATH RESULTS")
    print("-------------------")

    for step in result["steps"]:
        print(
            step["step_id"],
            step["description"],
            "APS:",
            step["attack_potential"]
        )

    print(
        "\nAFV:",
        result["attack_feasibility_value"]
    )

    print(
        "Feasibility:",
        result["attack_feasibility_rating"]
    )

    # 3. Calculate risk
    risk = calculate_risk(
        impact_rating="Severe",
        feasibility_rating=result["attack_feasibility_rating"]
    )

    print("Risk value:", risk)
