"""
Tests for Zoho API Client
"""

import pytest
from unittest.mock import Mock, patch
from app.core.zoho.client import ZohoClient
from app.core.zoho.auth import ZohoAuth

@pytest.fixture
def mock_auth():
    """Mock ZohoAuth instance"""
    auth = Mock(spec=ZohoAuth)
    auth.get_access_token.return_value = 'test_token'
    return auth

@pytest.fixture
def client(mock_auth):
    """Create ZohoClient instance with mocked auth"""
    with patch('app.core.zoho.client.ZohoAuth', return_value=mock_auth):
        client = ZohoClient()
        client.config = {
            'api_domain': 'https://test.zohoapis.com'
        }
        return client

def test_make_request_success(client, mock_auth):
    """Test successful API request"""
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_request.return_value = mock_response
        
        result = client._make_request('GET', '/test')
        
        assert result == {'data': 'test'}
        mock_request.assert_called_once()
        mock_auth.get_access_token.assert_called_once()

def test_make_request_token_refresh(client, mock_auth):
    """Test token refresh on 401 response"""
    with patch('requests.request') as mock_request:
        # First response with 401
        mock_response_401 = Mock()
        mock_response_401.status_code = 401
        
        # Second response after token refresh
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {'data': 'test'}
        
        mock_request.side_effect = [mock_response_401, mock_response_200]
        
        result = client._make_request('GET', '/test')
        
        assert result == {'data': 'test'}
        assert mock_request.call_count == 2
        assert mock_auth.get_access_token.call_count == 2
        mock_auth.invalidate_token.assert_called_once()

def test_make_request_error(client):
    """Test error handling in request"""
    with patch('requests.request') as mock_request:
        mock_request.side_effect = Exception('Test error')
        
        with pytest.raises(Exception) as exc:
            client._make_request('GET', '/test')
            
        assert str(exc.value) == 'Test error' 