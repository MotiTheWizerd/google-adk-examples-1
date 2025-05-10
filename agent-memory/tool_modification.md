## [2024-07-30] Enhanced network_info_tool with Shell Command Execution

Modified `tools/network_info_tool.py` to gather more advanced network information by executing platform-specific shell commands.

**Problem:** The existing `network_info_tool` primarily used `psutil` and lacked depth in areas like active connections, detailed routing, or OS-specific configurations that shell commands could provide.

**Fix:**

1.  Imported `subprocess` for running shell commands and `platform` for OS detection.
2.  Added a generic helper function `_run_shell_command(command_list)` that executes a given command, captures its stdout and stderr, and includes basic error handling (command not found, non-zero exit code, timeout).
3.  Integrated calls to `netstat -an` (for all OSes), `netsh` commands (for Windows, e.g., `netsh interface ipv4 show config`, `netsh interface ipv4 show dnsservers`), and `ip` / `ss` commands (for Linux, e.g., `ip addr`, `ip route`, `ss -tulnp`).
4.  The results from these commands are added to a new `advanced_info` dictionary within the main `network_details` structure returned by `get_network_info`.
    - `network_details['advanced_info']['netstat']`
    - `network_details['advanced_info']['netsh']` (Windows only)
    - `network_details['advanced_info']['linux_ip']` (Linux only)
5.  Currently, the output of these commands is stored as a list of raw output lines. Further parsing into structured Pydantic models could be a future enhancement.
6.  Updated relevant docstrings in `get_network_info`.

**Example of new structure in output:**

```python
{
    # ... other psutil based info ...
    'advanced_info': {
        'netstat': {
            'connections': [
                'Active Internet connections (servers and established)',
                'Proto Recv-Q Send-Q Local Address           Foreign Address         State',
                'tcp        0      0 127.0.0.1:5353          0.0.0.0:*               LISTEN',
                # ... more lines ...
            ],
            'error': None
        },
        'netsh': { # (Windows Example)
            'interface_ipv4_config': {
                 'output': [
                    'Configuration for interface "Ethernet"',
                    # ... more lines ...
                ],
                'error': None
            }
            # ... other netsh command outputs ...
        }
    }
}
```

**Lesson:** Tools within the ADK framework can be effectively extended by incorporating external command-line utilities. This allows access to a richer set of system information. Key considerations include: - Platform-specific command variations. - Robust error/exception handling for subprocesses. - Security implications if commands were to take user input (not the case here, as commands are predefined). - Deciding on the output format (raw vs. parsed structured data). For now, raw data is provided, with parsing as a potential next step.
