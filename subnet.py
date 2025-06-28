import json
from flask import Blueprint, request, jsonify
from src.utils.subnet_analyzer import analyze_subnet_allocation

subnet_bp = Blueprint('subnet', __name__)

@subnet_bp.route('/analyze', methods=['POST'])
def analyze_subnets():
    try:
        # Check if files are uploaded
        if 'big_block_file' not in request.files or 'allocated_subnets_file' not in request.files:
            return jsonify({'error': 'Both big_block_file and allocated_subnets_file are required'}), 400
        
        big_block_file = request.files['big_block_file']
        allocated_subnets_file = request.files['allocated_subnets_file']
        
        # Check if files are selected
        if big_block_file.filename == '' or allocated_subnets_file.filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        # Read and parse JSON files
        try:
            big_block_data = json.load(big_block_file)
            allocated_subnets_data = json.load(allocated_subnets_file)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400
        
        # Extract big block string
        if isinstance(big_block_data, dict) and 'big_block' in big_block_data:
            big_block_str = big_block_data['big_block']
        elif isinstance(big_block_data, str):
            big_block_str = big_block_data
        else:
            return jsonify({'error': 'Big block file should contain a "big_block" field or be a string'}), 400
        
        # Extract allocated subnets list
        if isinstance(allocated_subnets_data, dict) and 'allocated_subnets' in allocated_subnets_data:
            allocated_subnets_list = allocated_subnets_data['allocated_subnets']
        elif isinstance(allocated_subnets_data, list):
            allocated_subnets_list = allocated_subnets_data
        else:
            return jsonify({'error': 'Allocated subnets file should contain an "allocated_subnets" field or be a list'}), 400
        
        # Perform subnet analysis
        results = analyze_subnet_allocation(big_block_str, allocated_subnets_list)
        
        # Convert IPv4Network objects to strings for JSON serialization
        response_data = {
            'big_block': big_block_str,
            'total_ips_in_big_block': results['total_ips_in_big_block'],
            'total_allocated_ips': results['total_allocated_ips'],
            'total_free_ips': results['total_free_ips'],
            'allocated_subnets': [{'subnet': str(subnet), 'ip_count': subnet.num_addresses} for subnet in results['allocated_subnets']],
            'free_blocks': [{'subnet': str(block), 'ip_count': block.num_addresses} for block in results['free_blocks']]
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@subnet_bp.route('/analyze-json', methods=['POST'])
def analyze_subnets_json():
    """Alternative endpoint that accepts JSON data directly in the request body"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Extract big block and allocated subnets from JSON
        big_block_str = data.get('big_block')
        allocated_subnets_list = data.get('allocated_subnets')
        
        if not big_block_str:
            return jsonify({'error': 'big_block field is required'}), 400
        
        if not allocated_subnets_list or not isinstance(allocated_subnets_list, list):
            return jsonify({'error': 'allocated_subnets field is required and must be a list'}), 400
        
        # Perform subnet analysis
        results = analyze_subnet_allocation(big_block_str, allocated_subnets_list)
        
        # Convert IPv4Network objects to strings for JSON serialization
        response_data = {
            'big_block': big_block_str,
            'total_ips_in_big_block': results['total_ips_in_big_block'],
            'total_allocated_ips': results['total_allocated_ips'],
            'total_free_ips': results['total_free_ips'],
            'allocated_subnets': [{'subnet': str(subnet), 'ip_count': subnet.num_addresses} for subnet in results['allocated_subnets']],
            'free_blocks': [{'subnet': str(block), 'ip_count': block.num_addresses} for block in results['free_blocks']]
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

