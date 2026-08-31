# Jira MCP Client
# This client interacts with the Jira MCP Server to perform Jira operations.

from typing import Dict, Any, List, Optional
import json
import requests  # We'll use requests for HTTP communication with the MCP server
# Note: In a real system, we might use a different method (like gRPC) or a direct function call if the server is in-process.
# For this example, we assume the MCP server is running locally and we communicate via HTTP.

class JiraMCPClient:
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        # In a real system, we would handle authentication, etc.

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make an HTTP request to the MCP server.
        """
        url = f"{self.server_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        try:
            if method == "GET":
                response = requests.get(url, params=data, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # In a real system, we would handle errors appropriately.
            return {"success": False, "error": str(e)}

    def create_runtime_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", "/jira/create_runtime_task", params)

    def update_runtime_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", "/jira/update_runtime_task", params)

    def add_runtime_task_comment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", "/jira/add_runtime_task_comment", params)

    def search_tickets(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("GET", "/jira/search_tickets", params)

    def search_tickets_by_category(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("GET", "/jira/search_tickets_by_category", params)

    def get_ticket(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("GET", "/jira/get_ticket", params)

    def create_ticket(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", "/jira/create_ticket", params)

    def update_ticket(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", "/jira/update_ticket", params)

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Note: This example assumes the MCP server is running.
    # We'll just show how the client would be used.
    client = JiraMCPClient()
    # We cannot actually run the request without a server, so we'll just print the intended action.
    print("JiraMCPClient is ready to make requests to the MCP server.")