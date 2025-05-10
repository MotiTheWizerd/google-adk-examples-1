"""
Network Information Tool
------------------------

Provides functions to gather various network information details,
including interface addresses, MACs, status, and DNS servers.
"""
import socket
import psutil
import subprocess # Added import
import platform # Added import for OS detection

from google.adk.tools.tool_context import ToolContext # For ADK compatibility

def _run_shell_command(command: list[str]) -> tuple[str | None, str | None]:
    """
    Runs a shell command and returns its stdout and stderr.

    Args:
        command (list[str]): The command and its arguments as a list.

    Returns:
        tuple[str | None, str | None]: A tuple containing stdout and stderr.
                                       Returns (None, error_message) if command fails.
    """
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=15) # 15 seconds timeout
        if process.returncode != 0:
            return None, f"Command '{' '.join(command)}' failed with_code {process.returncode}: {stderr.strip()}"
        return stdout.strip(), None
    except FileNotFoundError:
        return None, f"Command '{command[0]}' not found."
    except subprocess.TimeoutExpired:
        return None, f"Command '{' '.join(command)}' timed out."
    except Exception as e:
        return None, f"Error running command '{' '.join(command)}': {str(e)}"

def _get_windows_netsh_info() -> dict:
    """
    Runs common 'netsh' commands on Windows and returns their output.
    """
    netsh_info = {}
    commands_to_run = {
        "interface_ipv4_config": ["netsh", "interface", "ipv4", "show", "config"],
        "interface_ipv6_config": ["netsh", "interface", "ipv6", "show", "config"],
        "dns_client_servers": ["netsh", "interface", "ipv4", "show", "dnsservers"], # Shows statically configured and via DHCP
        # Add other useful netsh commands here, e.g., for firewall, wireless profiles etc.
    }

    for key, command in commands_to_run.items():
        stdout, error = _run_shell_command(command)
        if error:
            netsh_info[key] = {"error": error}
        elif stdout:
            # Storing raw output, can be parsed further if needed.
            netsh_info[key] = {"output": stdout.splitlines()}
    return netsh_info

def _get_linux_ip_info() -> dict:
    """
    Runs common 'ip' and 'ss' commands on Linux and returns their output.
    """
    linux_info = {}
    commands_to_run = {
        "ip_addr": ["ip", "addr"],
        "ip_route": ["ip", "route"],
        "ss_listening_ports": ["ss", "-tulnp"] # Show TCP/UDP listening, no resolve, numeric ports, process
    }

    for key, command in commands_to_run.items():
        stdout, error = _run_shell_command(command)
        if error:
            linux_info[key] = {"error": error}
        elif stdout:
            linux_info[key] = {"output": stdout.splitlines()}
    return linux_info

def _get_netstat_info() -> dict:
    """
    Runs 'netstat -an' and returns parsed information.
    Placeholder for more detailed parsing.
    """
    netstat_data = {"connections": None, "error": None}
    command = ["netstat", "-an"]
    stdout, error = _run_shell_command(command)

    if error:
        netstat_data["error"] = error
    elif stdout:
        # Basic parsing: just store the raw output for now.
        # In a real scenario, you'd parse this into a structured format.
        netstat_data["connections"] = stdout.splitlines()
    return netstat_data

def get_network_info(tool_context: ToolContext = None) -> dict:
    """
    Gathers detailed network information, including advanced details from shell commands.

    Args:
        tool_context (ToolContext, optional): ADK tool context. Defaults to None.
                                              Not actively used in this function but
                                              included for ADK compatibility.

    Returns:
        dict: Network information (hostname, interface details, DNS servers, advanced_info, etc.)
    """
    network_details = {
        'hostname': socket.gethostname(),
        'interfaces': {},
        'dns_servers': [],
        'advanced_info': {}, # Added key for advanced details
        'notes': []
    }

    # Get interface addresses (IP, MAC)
    try:
        all_interfaces = psutil.net_if_addrs()
        for interface_name, interface_addresses in all_interfaces.items():
            network_details['interfaces'][interface_name] = {'addresses': [], 'stats': {}}
            for addr in interface_addresses:
                addr_info = {'family': str(addr.family)}
                if addr.family == socket.AF_INET: # IPv4
                    addr_info['address'] = addr.address
                    addr_info['netmask'] = addr.netmask
                    addr_info['broadcast'] = addr.broadcast
                elif addr.family == socket.AF_INET6: # IPv6
                    # For IPv6, netmask and broadcast might not be as straightforward or universally present/named
                    addr_info['address'] = addr.address
                    if hasattr(addr, 'netmask') and addr.netmask: # Netmask for IPv6 is often prefix length
                         addr_info['netmask'] = addr.netmask
                elif hasattr(psutil, 'AF_LINK') and addr.family == psutil.AF_LINK: # MAC Address
                    addr_info['type'] = 'MAC'
                    addr_info['address'] = addr.address
                else:
                    addr_info['address'] = addr.address

                network_details['interfaces'][interface_name]['addresses'].append(addr_info)
    except Exception as e:
        network_details['errors_interfaces_addresses'] = str(e)

    # Get interface statistics (isup, duplex, speed, mtu)
    try:
        all_stats = psutil.net_if_stats()
        for interface_name, stat_info in all_stats.items():
            if interface_name in network_details['interfaces']:
                network_details['interfaces'][interface_name]['stats'] = {
                    'is_up': stat_info.isup,
                    'duplex': str(stat_info.duplex),
                    'speed_mbps': stat_info.speed,
                    'mtu': stat_info.mtu
                }
            else: # Should not happen if all_interfaces was comprehensive
                 network_details['interfaces'][interface_name] = {'addresses': [], 'stats': {
                    'is_up': stat_info.isup,
                    'duplex': str(stat_info.duplex),
                    'speed_mbps': stat_info.speed,
                    'mtu': stat_info.mtu
                }}
    except Exception as e:
        network_details['errors_interfaces_stats'] = str(e)

    # Attempt to get DNS servers (platform-dependent and can be complex)
    # This is a simplified approach. Production tools might use platform-specific APIs or parse command outputs.
    dns_note = "DNS server retrieval is platform-dependent and this basic tool uses a simplified approach. Results may vary."
    network_details['notes'].append(dns_note)
    try:
        if hasattr(psutil, 'WINDOWS') and psutil.WINDOWS:
            # For Windows, parsing 'ipconfig /all' or using WMI/powershell is more reliable.
            # This is a placeholder, as direct psutil method isn't available.
            network_details['notes'].append("On Windows, DNS info via this tool is limited. Consider using 'ipconfig /all' for confirmation.")
            # A common but less robust way for Windows if other methods fail:
            # import winreg
            # key_path = r"SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces"
            # try:
            #     with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as interfaces_key:
            #         # Iterate subkeys (each interface)
            #         # Look for 'NameServer' or 'DhcpNameServer'
            # except Exception:
            #     pass # Fallback to other methods or note
        elif hasattr(psutil, 'LINUX') and psutil.LINUX:
            try:
                with open("/etc/resolv.conf", "r") as f:
                    for line in f:
                        if line.strip().startswith("nameserver"):
                            dns_server = line.strip().split(maxsplit=1)[1]
                            if dns_server not in network_details['dns_servers']:
                                network_details['dns_servers'].append(dns_server)
            except FileNotFoundError:
                network_details['notes'].append("Could not find /etc/resolv.conf for DNS servers on Linux.")
            except Exception as e_dns_linux:
                 network_details['errors_dns_linux'] = str(e_dns_linux)
        elif hasattr(psutil, 'MACOS') and psutil.MACOS:
            # On macOS, 'scutil --dns' output parsing is common.
            network_details['notes'].append("On macOS, DNS info via this tool is limited. Consider using 'scutil --dns' for confirmation.")
        else:
            network_details['notes'].append("DNS server retrieval not specifically implemented for this OS in the basic tool.")

    except Exception as e_dns:
        network_details['errors_dns_general'] = str(e_dns)

    # Gather advanced network information using shell commands
    network_details['advanced_info']['netstat'] = _get_netstat_info()
    
    current_os = platform.system().lower()
    if current_os == "windows":
        network_details['advanced_info']['netsh'] = _get_windows_netsh_info()
    elif current_os == "linux":
        network_details['advanced_info']['linux_ip'] = _get_linux_ip_info()
        # Note: netstat is still run for all OS types, but ss provides more modern info for Linux.

    return network_details
