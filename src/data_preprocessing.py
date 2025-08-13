import pandas as pd
import numpy as np

def remove_outliers(df, column, n_std=2.5):
    """Remove outliers based on standard deviation"""
    mean = df[column].mean()
    std = df[column].std()
    return df[(df[column] <= mean + (n_std * std)) & 
             (df[column] >= mean - (n_std * std))]

def check_data_quality(df):
    """Check data quality and print summary"""
    print("=== Data Quality Report ===")
    
    # Check data types
    print("\nData Types:")
    print(df.dtypes.value_counts())
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        print("\nColumns with missing values:")
        print(missing[missing > 0])
    else:
        print("\nNo missing values found!")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"\nNumber of duplicate rows: {duplicates}")
    
    # Check numerical columns for invalid values
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    print("\nChecking numerical columns for invalid values...")
    for col in numeric_cols:
        invalid = df[df[col] < 0].shape[0]  # Assuming negative values are invalid
        if invalid > 0:
            print(f"- {col}: {invalid} negative values found")
            
    return {'missing': missing, 'duplicates': duplicates}

def prepare_data(df):
    """Prepare data by handling missing values and outliers"""
    try:
        print("Starting data preparation...")
        
        # First, check data quality
        quality_report = check_data_quality(df)
        
        # Remove outliers from the SalePrice column
        print("\nRemoving outliers from SalePrice...")
        original_size = len(df)
        df = remove_outliers(df, 'SalePrice', n_std=2.5)
        removed_count = original_size - len(df)
        print(f"Removed {removed_count} outliers ({(removed_count/original_size)*100:.2f}% of data)")
        
        # Handle missing values
        print("\nHandling missing values...")
        # For numerical columns, fill with median
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
                
        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        # Verify no missing values remain
        remaining_missing = df.isnull().sum().sum()
        print(f"Remaining missing values: {remaining_missing}")
        
        print("\nData preparation completed!")
        
        # Display the shape of the cleaned dataset
        print(f"\nFinal dataset shape: {df.shape}")
        
        return df
        
    except Exception as e:
        print(f"Error during data preparation: {str(e)}")
        return None
