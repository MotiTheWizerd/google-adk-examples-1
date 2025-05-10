"""
System Information Tool
-----------------------

Provides a function to gather various system information details.
This tool can be used to collect data about the operating system,
hardware (CPU, RAM), Python version, and network hostname.

It leverages the `psutil` library for more detailed information if available,
falling back to standard library modules like `platform`, `os`, and `socket`
for basic information.
"""
import os
import platform
import socket

import psutil

from google.adk.tools.tool_context import ToolContext


def get_system_info(tool_context: ToolContext = None) -> dict:
    """
    Gather important system information.
    Uses psutil for detailed info if available, otherwise falls back to stdlib.

    Args:
        tool_context (ToolContext, optional): ADK tool context. Defaults to None.
                                              Not actively used in this function but
                                              included for ADK compatibility.
    Returns:
        dict: System information (OS, Python version, CPU, RAM, hostname, etc.)
    """
    info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'hostname': socket.gethostname(),
    }
    # Try to use psutil for more detailed information if it's installed
    try:
        # We check if psutil is available (imported successfully)
        # and then use it. If it wasn't imported, this block will be skipped.
        info['cpu_count'] = psutil.cpu_count(logical=True)  # Number of logical CPUs
        info['memory_total_gb'] = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # Total RAM in GB
        info['memory_available_gb'] = round(psutil.virtual_memory().available / (1024 ** 3), 2)  # Available RAM in GB
        info['boot_time'] = psutil.boot_time()  # System boot time (timestamp)
    except (NameError, AttributeError):
        # Fallback if psutil is not available or an attribute is missing
        # (though NameError is more likely if import psutil fails silently or is conditional)
        info['cpu_count'] = os.cpu_count()  # Number of CPUs from os module
        info['memory_total_gb'] = None  # Not reliably available without psutil
        info['memory_available_gb'] = None # Not reliably available without psutil
        info['boot_time'] = None # Not available without psutil
    return info
