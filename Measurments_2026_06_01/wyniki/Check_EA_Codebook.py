import pandas as pd
import numpy as np
import ast
import os

# 1. Define your parameters
SEPARATOR = ';'                  
SLICE_START = 224                  
SLICE_END = 1824                    
SLICE_STEP = 2
TOLERANCE = 5

def process_csv_lists(file_path: str):
    # 2. Load the CSV file
    df = pd.read_csv(file_path, sep=SEPARATOR, index_col=False)
    print("Columns found in file 1:", df.keys())
    
    # 3. Convert the 'trace' column from string to actual Python lists
    # Note: Make sure the space in ' trace' perfectly matches your CSV header!
    df[' trace'] = df[' trace'].apply(ast.literal_eval)
    
    # 4. Slice the lists according to your truncation needs
    df['sliced_trace'] = df[' trace'].apply(lambda x: x[SLICE_START:SLICE_END:SLICE_STEP])
    
    # 5. Convert to 2D numpy array
    list_matrix = np.array(df['sliced_trace'].tolist())
    
    # 6. Find the max indices and exact max values
    max_row_indices = np.argmax(list_matrix, axis=0)
    max_values = np.max(list_matrix, axis=0)
    
    # 7. Extract the corresponding IDs and Rx_angles
    highest_ids = (df['N'].iloc[max_row_indices]).tolist()
    highest_rx_angles = df[' Beta'].iloc[max_row_indices].tolist()
    
    # 8. Compile the results
    results_df = pd.DataFrame({
        'highest_id': highest_ids,
        'Rx_angle': highest_rx_angles,
        'max_value': max_values
    })
    
    # Safely construct the save path so it doesn't break on absolute paths
    save_dir = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    save_name = 'best_patts_' + base_name
    
    # Recombine directory and new filename
    save_path = os.path.join(save_dir, save_name) if save_dir else save_name
    
    results_df.to_csv(save_path, index=False)
    print(f"Results saved safely to: {save_path}")
    
    # Return the save path so the next function can easily find it
    return save_path


def compare_rx_angles(results_file: str, codebook: str):
    # 2. Load the results file
    print(results_file)
    df_results = pd.read_csv(results_file)
    
    # 3. Load the second file WITHOUT headers
    df_second = pd.read_csv(
        codebook, 
        sep=';', 
        header=None, 
        usecols=[0, 1, 2],
        names=['id', 'Pat', 'measurements']
    )
    
    # 4. Convert strings to lists
    df_second['measurements'] = df_second['measurements'].apply(ast.literal_eval)
    
    # --- CRITICAL FIX: Force both ID columns to be strings so they merge perfectly ---
    df_results['highest_id'] = df_results['highest_id'].astype(str)
    df_second['id'] = df_second['id'].astype(str)
    
    # 5. Merge the DataFrames
    merged_df = pd.merge(df_results, df_second, left_on='highest_id', right_on='id', how='inner')
    
    print(f"Rows after merge: {len(merged_df)}")
    if len(merged_df) == 0:
        print("WARNING: The merged dataset is empty. Check your CSVs to ensure the IDs actually match.")
    
    # 6. Loop to find close Rx values
    has_match_list = []
    matched_rx_list = []
    
    for index, row in merged_df.iterrows():
        target_rx = row['Rx_angle']
        measurements = row['measurements']
        matching_rxs = []
        
        if isinstance(measurements, list):
            for sublist in measurements:
                if len(sublist) >= 2:          
                    rx_val = sublist[1]
                    if abs(rx_val - target_rx) <= TOLERANCE:
                        matching_rxs.append(rx_val)
                        
        has_match_list.append(len(matching_rxs) > 0)
        matched_rx_list.append(matching_rxs)

    # 7. Assign new columns
    merged_df['has_match'] = has_match_list
    merged_df['matched_rx_values'] = matched_rx_list
    
    # 8. Print and save final results
    print("\nPreview of matches:")
    print(merged_df[['highest_id', 'Rx_angle', 'has_match', 'matched_rx_values']].head())
    
    path_to_save = os.path.dirname(results_file)
    file_name = 'rx_comparison_'+results_file.split('\\')[-1]
    merged_df.to_csv(os.path.join(path_to_save,file_name), index=False)
    print("\nResults saved to:: rx_comparison_"+results_file)

if __name__ == "__main__":
    cd_path = os.getcwd()
    parent_dir = os.path.dirname(cd_path)
    codebook_dir = os.path.join(parent_dir, 'codebooks')
    for i in range(3):
        process_csv_lists(f"PK_codebook_final_-15_0_0_90_01_Jun_2026_{i+1}.csv")
        compare_rx_angles(f"best_patts_PK_codebook_final_-15_0_0_90_01_Jun_2026_{i+1}.csv", os.path.join(codebook_dir, "PK_codebook_final_-15_0_0_90.csv"))