"""
CSV reading module for parsing customer data.
Handles column mapping to standardize field names.
"""

import pandas as pd


def read_customers(csv_path, column_map):
    """
    Read customers from CSV file and map columns to standard field names.
    
    Args:
        csv_path: Path to CSV file
        column_map: Dictionary mapping standard fields to CSV column names
                   e.g., {'email': 'email', 'vorname': 'vorname', 'nachname': 'nachname', 'anrede': 'anrede', 'du': 'du'}
    
    Returns:
        List of dictionaries, each containing customer data with standardized keys
        e.g., [{'email': '...', 'vorname': '...', 'nachname': '...', 'anrede': '...', 'du': '...'}, ...]
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Map columns to standard field names
        customers = []
        for _, row in df.iterrows():
            customer = {}
            for standard_field, csv_column in column_map.items():
                if csv_column in df.columns:
                    customer[standard_field] = row[csv_column]
                else:
                    customer[standard_field] = None
            
            # Only add if email exists
            if customer.get('email'):
                customers.append(customer)
        
        return customers
    
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

