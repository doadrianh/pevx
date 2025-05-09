import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from pevx.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    """Test that CLI shows help message."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Prudentia CLI' in result.output
    assert 'auth-poetry' in result.output

@patch('subprocess.run')
def test_auth_poetry_command(mock_run, runner):
    """Test auth-poetry command with mocked subprocess calls."""
    # Mock the AWS CLI token response
    mock_process = MagicMock()
    mock_process.stdout = "fake-token"
    mock_process.returncode = 0
    mock_run.return_value = mock_process
    
    # Run the command
    result = runner.invoke(cli, ['auth-poetry'])
    
    # Check that the command ran successfully
    assert result.exit_code == 0
    assert "Authenticating poetry with AWS CodeArtifact" in result.output
    
    # Verify AWS CLI and poetry commands were called with expected arguments
    expected_calls = [
        # AWS CodeArtifact get-authorization-token call
        ([
            'aws', 'codeartifact', 'get-authorization-token',
            '--domain', 'prudentia-sciences',
            '--domain-owner', '728222516696',
            '--region', 'us-east-1',
            '--query', 'authorizationToken',
            '--output', 'text'
        ],),
        # Poetry source remove call
        (['poetry', 'source', 'remove', 'codeartifact'],),
        # Poetry source add call
        (['poetry', 'source', 'add', 'codeartifact', 
          'https://prudentia-sciences-728222516696.d.codeartifact.us-east-1.amazonaws.com/pypi/pypi-store/simple/'],),
        # Poetry config call
        (['poetry', 'config', 'http-basic.codeartifact', 'aws', 'fake-token'],)
    ]
    
    # Check that subprocess.run was called with expected arguments
    assert mock_run.call_count >= 4
    for i, expected_args in enumerate(expected_calls):
        if i < len(mock_run.call_args_list):
            actual_args = mock_run.call_args_list[i][0]
            assert actual_args[0] == expected_args[0] 