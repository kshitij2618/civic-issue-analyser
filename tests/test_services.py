from backend.services.authority_service import (
    get_authority_by_issue_code
)


def test_pothole_authority():

    result = get_authority_by_issue_code(
        "ROAD_POTHOLE"
    )

    print("\nPOTHOLE RESULT:")
    print(result)

    assert result["matched"] is True

    assert (
        result["authority"]["department"]
        == "Road Maintenance Department"
    )


def test_electrical_hazard():

    result = get_authority_by_issue_code(
        "ELECTRICAL_HAZARD"
    )

    print("\nELECTRICAL RESULT:")
    print(result)

    assert result["matched"] is True

    assert (
        result["authority"]["department"]
        == "Electrical Safety / Distribution Department"
    )


def test_unknown_issue():

    result = get_authority_by_issue_code(
        "THIS_DOES_NOT_EXIST"
    )

    assert result["matched"] is False
    assert result["authority"] is None