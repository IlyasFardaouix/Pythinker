from pydantic import BaseModel, Field

class GitRemoteSpec(BaseModel):
    """
    Represents a Git remote specification.
    """
    repo_url: str | None = None  # URL of the Git repository
    remote_name: str | None = None  # Name of the remote
    branch: str | None = None  # Branch to clone
    credentials: dict[str, str] | None = None  # Credentials for authentication


class WorkspaceManifest(BaseModel):
    """
    Represents a workspace manifest.
    """
    name: str | None = None  # Name of the workspace
    path: str | None = None  # Path to the workspace
    template_id: str | None = None  # ID of the template used
    capabilities: list[str] = Field(default_factory=list)  # List of capabilities
    dev_command: str | None = None  # Development command
    build_command: str | None = None  # Build command
    test_command: str | None = None  # Test command
    port: int | None = None  # Port number
    env_vars: dict[str, str] = Field(default_factory=dict)  # Environment variables
    secrets: dict[str, str] = Field(default_factory=dict)  # Secrets
    files: dict[str, str] = Field(default_factory=dict)  # Files
    git_remote: 'GitRemoteSpec' | None = None  # Git remote specification


class WorkspaceWriteError(BaseModel):
    """
    Represents a workspace write error.
    """
    path: str  # Path where the error occurred
    message: str  # Error message


class WorkspaceManifestResponse(BaseModel):
    """
    Represents a workspace manifest response.
    """
    session_id: str  # Session ID
    workspace_root: str  # Workspace root
    project_root: str  # Project root
    project_name: str  # Project name
    project_path: str | None = None  # Project path
    template_id: str | None = None  # ID of the template used
    template_used: str | None = None  # Template used
    capabilities: list[str] = Field(default_factory=list)  # List of capabilities
    files_written: int = 0  # Number of files written
    files_failed: int = 0  # Number of files failed
    write_errors: list[WorkspaceWriteError] = Field(default_factory=list)  # List of write errors
    env_var_keys: list[str] = Field(default_factory=list)  # Environment variable keys
    secret_keys: list[str] = Field(default_factory=list)  # Secret keys
    dev_command: str | None = None  # Development command
    build_command: str | None = None  # Build command
    test_command: str | None = None  # Test command
    port: int | None = None  # Port number
    git_remote: 'GitRemoteSpec' | None = None  # Git remote specification
    git_clone_success: bool | None = None  # Git clone success
    git_clone_message: str | None = None  # Git clone message
```

```python
# No imports needed

def main():
    # Your code here

if __name__ == "__main__":
    main()