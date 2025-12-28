import datetime

def get_mock_violations():
    """
    Returns a list of structured violation data simulating what the AI would extract.
    """
    return [
        {
            "facility_name": "Sunrise Valley Farms",
            "violation_date": (datetime.date.today() - datetime.timedelta(days=2)).isoformat(),
            "violation_type": "Inhumane Handling",
            "location": "Springfield, IL",
            "summary": "Observation of excessive force used during loading of livestock.",
            "latitude": 39.7817, # Mock coords for map
            "longitude": -89.6501
        },
        {
            "facility_name": "Midwest Meat Processing",
            "violation_date": (datetime.date.today() - datetime.timedelta(days=5)).isoformat(),
            "violation_type": "Sanitation Defect",
            "location": "Ames, IA",
            "summary": "Failure to maintain sanitary conditions in the slaughter area.",
            "latitude": 42.0308,
            "longitude": -93.6319
        },
        {
            "facility_name": "Happy Cows Dairy (Irony)",
            "violation_date": (datetime.date.today() - datetime.timedelta(days=10)).isoformat(),
            "violation_type": "Water Pollution",
            "location": "Fresno, CA",
            "summary": "Unauthorized discharge of wastewater into local stream.",
            "latitude": 36.7378,
            "longitude": -119.7871
        }
    ]
