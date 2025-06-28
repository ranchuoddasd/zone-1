
import ipaddress

def analyze_subnet_allocation(big_block_str, allocated_subnets_str):
    """
    Analyzes subnet allocation within a large network block.

    Args:
        big_block_str (str): The large network block in CIDR notation (e.g., '10.10.0.0/16').
        allocated_subnets_str (list): A list of allocated subnets in CIDR notation.

    Returns:
        dict: A dictionary containing:
            - 'total_ips_in_big_block': Total number of IP addresses in the big block.
            - 'total_allocated_ips': Total number of allocated IP addresses.
            - 'total_free_ips': Total number of free IP addresses.
            - 'allocated_subnets': List of allocated subnets (ipaddress.IPv4Network objects).
            - 'free_blocks': List of free contiguous blocks (ipaddress.IPv4Network objects).
    """
    big_block = ipaddress.ip_network(big_block_str)
    allocated_networks = [ipaddress.ip_network(s, strict=False) for s in allocated_subnets_str]

    total_ips_in_big_block = big_block.num_addresses
    total_allocated_ips = 0

    # Sort allocated networks to handle overlaps and make processing easier
    allocated_networks.sort(key=lambda x: x.network_address)

    # Calculate total allocated IPs and merge overlapping/contiguous allocated blocks
    merged_allocated_networks = []
    if allocated_networks:
        current_merge = allocated_networks[0]
        for i in range(1, len(allocated_networks)):
            # Check if the current allocated network is contiguous or overlaps with the current_merge
            # A network is contiguous if its network address is the broadcast address of the previous + 1
            if allocated_networks[i].overlaps(current_merge) or \
               allocated_networks[i].network_address == current_merge.broadcast_address + 1:
                # Merge if overlaps or is contiguous
                # Use ipaddress.collapse_addresses to get the smallest possible list of networks that cover the given networks
                # This handles cases where networks are adjacent but not overlapping, and summarizes them if possible
                collapsed = list(ipaddress.collapse_addresses([current_merge, allocated_networks[i]]))
                if len(collapsed) == 1:
                    current_merge = collapsed[0]
                else:
                    # If collapse_addresses returns more than one network, it's not contiguous
                    # or cannot be summarized into a single block. Add current_merge and start new.
                    merged_allocated_networks.append(current_merge)
                    current_merge = allocated_networks[i]
            else:
                merged_allocated_networks.append(current_merge)
                current_merge = allocated_networks[i]
        merged_allocated_networks.append(current_merge)
    
    for net in merged_allocated_networks:
        total_allocated_ips += net.num_addresses

    total_free_ips = total_ips_in_big_block - total_allocated_ips

    # Find free blocks
    free_blocks = []
    current_ip = big_block.network_address

    for allocated_net in merged_allocated_networks:
        if current_ip < allocated_net.network_address:
            # There's a free block before the current allocated_net
            free_range_start = current_ip
            free_range_end = allocated_net.network_address - 1
            # Attempt to summarize the free range into the largest possible CIDR blocks
            for free_net in ipaddress.summarize_address_range(free_range_start, free_range_end):
                free_blocks.append(free_net)
        current_ip = allocated_net.broadcast_address + 1

    # Check for any remaining free space after the last allocated block
    if current_ip <= big_block.broadcast_address:
        free_range_start = current_ip
        free_range_end = big_block.broadcast_address
        for free_net in ipaddress.summarize_address_range(free_range_start, free_range_end):
            free_blocks.append(free_net)

    return {
        'total_ips_in_big_block': total_ips_in_big_block,
        'total_allocated_ips': total_allocated_ips,
        'total_free_ips': total_free_ips,
        'allocated_subnets': merged_allocated_networks,
        'free_blocks': free_blocks
    }

if __name__ == '__main__':
    # Example Usage:
    big_block = '10.10.0.0/16'
    allocated_subnets = [
        '10.10.0.0/24',  # 256 IPs
        '10.10.1.0/24',  # 256 IPs
        '10.10.3.0/24',  # 256 IPs (leaving 10.10.2.0/24 free)
        '10.10.5.0/24',  # 256 IPs (leaving 10.10.4.0/24 free)
        '10.10.10.0/23', # 512 IPs
        '10.10.20.0/22', # 1024 IPs
        '10.10.24.0/21', # 2048 IPs
        '10.10.32.0/20', # 4096 IPs
        '10.10.64.0/19', # 8192 IPs
        '10.10.128.0/18', # 16384 IPs
        '10.10.0.0/17'  # Corrected: A /17 block, valid network address
    ]

    results = analyze_subnet_allocation(big_block, allocated_subnets)

    print(f"Big Block: {big_block}")
    print(f"Total IPs in Big Block: {results['total_ips_in_big_block']}")
    print(f"Total Allocated IPs: {results['total_allocated_ips']}")
    print(f"Total Free IPs: {results['total_free_ips']}")

    print("\nAllocated Subnets (merged and sorted):")
    for subnet in results['allocated_subnets']:
        print(f"- {subnet} ({subnet.num_addresses} IPs)")

    print("\nFree Blocks:")
    if results['free_blocks']:
        for block in results['free_blocks']:
            print(f"- {block} ({block.num_addresses} IPs)")
    else:
        print("No free blocks found.")


