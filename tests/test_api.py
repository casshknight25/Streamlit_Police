import pytest
import requests_mock
from utils.api import handle_point_geometry, handle_polygon_geometry, get_crime_data

@pytest.fixture
def mock_requests():
    """Fixture to set up requests-mock for mocking HTTP requests."""
    with requests_mock.Mocker() as m:
        yield m

def test_handle_point_geometry(mock_requests):
    """Test handling of Point geometry."""
    # Mock response data similar to the expected API response
    mock_response_data = [
        {
            "category": "anti-social-behaviour",
            "location": {"latitude": "55.9533", "longitude": "-3.1882"},
            "outcome_status": {"category": "investigation complete; no suspect identified"}
        },
        {
            "category": "violent-crime",
            "location": {"latitude": "55.9533", "longitude": "-3.1882"},
            "outcome_status": {"category": "court result"}
        }
    ]
    mock_requests.post('https://data.police.uk/api/crimes-street/all-crime?lat=55.9533&lng=-3.1882', json=mock_response_data)

    feature = {
        "geometry": {
            "type": "Point",
            "coordinates": [-3.1882, 55.9533]
        }
    }

    data = handle_point_geometry(feature)
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 2  # Check if both mock records are returned

def test_handle_polygon_geometry(mock_requests):
    """Test handling of Polygon geometry."""
    # Mock response data similar to the expected API response
    mock_response_data = [
        {
            "category": "burglary",
            "location": {"latitude": "55.9533", "longitude": "-3.1882"},
            "outcome_status": {"category": "under investigation"}
        },
        {
            "category": "public-order",
            "location": {"latitude": "55.9533", "longitude": "-3.1882"},
            "outcome_status": {"category": "court result"}
        }
    ]
    # Mock the POST request
    mock_requests.post('https://data.police.uk/api/crimes-street/all-crime', json=mock_response_data)

    feature = {
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[-3.1882, 55.9533], [-3.1882, 56.9533], [-3.1882, 55.9533]]]
        }
    }

    data = handle_polygon_geometry(feature)
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 2  # Check if both mock records are returned

def test_get_crime_data(mock_requests):
    """Test fetching crime data from the API."""
    # Mock response data similar to the expected API response
    mock_response_data = [
        {
            "category": "violent-crime",
            "location": {"latitude": "55.9533", "longitude": "-3.1882"},
            "outcome_status": {"category": "court result"}
        },
        {
            "category": "anti-social-behaviour",
            "location": {"latitude": "55.9533", "longitude": "-3.1882"},
            "outcome_status": {"category": "investigation complete; no suspect identified"}
        }
    ]
    mock_requests.post('https://data.police.uk/api/crimes-street/all-crime?lat=55.9533&lng=-3.1882', json=mock_response_data)

    url = 'https://data.police.uk/api/crimes-street/all-crime?lat=55.9533&lng=-3.1882'
    data = get_crime_data(url)
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 2  # Check if both mock records are returned
