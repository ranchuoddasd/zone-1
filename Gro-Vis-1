import networkx as nx
import matplotlib.pyplot as plt
from ciscoconfparse import CiscoConfParse
import re
import io
import platform  # Added missing import

# Sample configurations
cisco_config = """
interface FastEthernet0/1
 ip address 172.16.1.2 255.255.255.252
 ip policy route-map PBR
!
access-list 101 permit ip 192.168.10.0 0.0.0.255 200.100.30.248 0.0.0.7
!
route-map PBR permit 10
 match ip address 101
 set community 65000:100
 set next-hop 192.168.1.1
!
router bgp 65000
 neighbor 172.16.1.1 remote-as 65001
 neighbor 172.16.1.1 send-community
"""

juniper_config = """
interfaces {
    ge-0/0/1 {
        unit 0 {
            family inet {
                address 172.16.1.1/30;
                filter input FBF-FILTER;
            }
        }
    }
}
firewall {
    family inet {
        filter FBF-FILTER {
            term block-subnet {
                from {
                    source-address {
                        192.168.10.0/24;
                    }
                }
                then {
                    discard;
                }
            }
            term accept-all {
                then accept;
            }
        }
    }
}
policy-options {
    prefix-list customers {
        172.16.1.0/24;
    }
    policy-statement BGP-EXPORT {
        term export-customers {
            from {
                prefix-list customers;
            }
            then {
                community add export-comm;
                accept;
            }
        }
    }
    community export-comm members 65000:100;
}
protocols {
    bgp {
        group ext {
            neighbor 172.16.1.2 {
                export BGP-EXPORT;
            }
        }
    }
}
"""


# Parse configurations
def parse_config(config_text, platform="cisco"):
    if platform == "cisco":
        parse = CiscoConfParse(config_text.splitlines())
        return parse
    elif platform == "juniper":
        # Simulate Juniper parsing (ciscoconfparse doesn't fully support Junos, so use regex for simplicity)
        config_dict = {
            "interfaces": [],
            "firewall_filters": [],
            "prefix_lists": [],
            "communities": [],
            "route_policies": []
        }
        lines = config_text.splitlines()
        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith("interfaces"):
                current_section = "interfaces"
            elif line.startswith("firewall"):
                current_section = "firewall_filters"
            elif line.startswith("policy-options"):
                current_section = "policy-options"
            elif line.startswith("protocols"):
                current_section = "protocols"
            elif current_section and line:
                if current_section == "policy-options" and "prefix-list" in line:
                    config_dict["prefix_lists"].append(line)
                elif current_section == "policy-options" and "community" in line:
                    config_dict["communities"].append(line)
                elif current_section == "policy-options" and "policy-statement" in line:
                    config_dict["route_policies"].append(line)
                elif current_section == "firewall" and "filter" in line:
                    config_dict["firewall_filters"].append(line)
        return config_dict


# Analyze impact
def analyze_impact(cisco_parse, juniper_config_dict, topology):
    impact_report = []

    # Cisco route-map and ACL impact
    acls = cisco_parse.find_objects(r"^access-list")
    route_maps = cisco_parse.find_objects(r"^route-map")
    for rm in route_maps:
        match = rm.re_search_children(r"match ip address")
        set_comm = rm.re_search_children(r"set community")
        set_nh = rm.re_search_children(r"set next-hop")
        if match and set_comm:
            acl_id = match[0].text.split()[-1]
            acl = next((a for a in acls if a.text.split()[1] == acl_id), None)
            if acl:
                impact_report.append(
                    f"Cisco Route-Map {rm.text}: Matches {acl.text}, sets community {set_comm[0].text.split()[-1]}")
                impact_report.append(
                    f"Impact: Routes from 192.168.10.0/24 to 200.100.30.248/29 redirected to next-hop 192.168.1.1")
                for node in topology.neighbors("R1"):
                    impact_report.append(
                        f"Neighbor {node}: Receives routes with community 65000:100, may alter BGP decisions")

    # Juniper firewall filter and prefix list impact
    filters = juniper_config_dict.get("firewall_filters", [])
    for f in filters:
        if "discard" in f:
            impact_report.append(f"Juniper Filter {f}: Discards traffic from 192.168.10.0/24")
            for node in topology.neighbors("R2"):
                impact_report.append(f"Neighbor {node}: Traffic from 192.168.10.0/24 to {node} blocked")

    prefix_lists = juniper_config_dict.get("prefix_lists", [])
    for pl in prefix_lists:
        if "172.16.1.0/24" in pl:
            impact_report.append(f"Juniper Prefix-List {pl}: Exports 172.16.1.0/24 with community 65000:100")
            for node in topology.neighbors("R2"):
                impact_report.append(f"Neighbor {node}: Receives 172.16.1.0/24 with community, may influence routing")

    return impact_report


# Visualize network and flow
def visualize_network(topology, impacted_nodes, impacted_edges):
    pos = nx.spring_layout(topology)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(topology, pos, node_color="lightblue", node_size=500)
    nx.draw_networkx_nodes(topology, pos, nodelist=impacted_nodes, node_color="red", node_size=500)
    nx.draw_networkx_edges(topology, pos, edge_color="gray")
    nx.draw_networkx_edges(topology, pos, edgelist=impacted_edges, edge_color="red", width=2)
    nx.draw_networkx_labels(topology, pos)
    plt.title("Network Flow Impact")
    plt.axis("off")
    # Save the visualization to a file for local execution
    plt.savefig("network_impact.png", format="png")
    plt.close()
    return "Visualization saved as network_impact.png"


# Main function
def main():
    # Create network topology
    G = nx.Graph()
    G.add_nodes_from(["R1", "R2", "R3"])
    G.add_edges_from([("R1", "R2"), ("R2", "R3"), ("R1", "R3")])

    # Parse configurations
    cisco_parse = parse_config(cisco_config, "cisco")
    juniper_parse = parse_config(juniper_config, "juniper")

    # Analyze impact
    impact_report = analyze_impact(cisco_parse, juniper_parse, G)

    # Identify impacted nodes and edges
    impacted_nodes = ["R1", "R2"]  # Devices with new configs
    impacted_edges = [("R1", "R2"), ("R2", "R3")]  # Affected paths

    # Visualize
    viz_result = visualize_network(G, impacted_nodes, impacted_edges)

    # Generate configuration preview
    config_preview = f"""
Cisco Configuration (R1):
{cisco_config}

Juniper Configuration (R2):
{juniper_config}

Impact Report:
{chr(10).join(impact_report)}

{viz_result}
"""
    return config_preview


# Run main function
if __name__ == "__main__":
    result = main()
    print(result)
