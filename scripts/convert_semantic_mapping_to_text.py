# scripts/convert_semantic_mapping_to_text.py
import json
import os
import sys

# Tentukan path relatif dari root proyek
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_JSON_PATH = os.path.join(project_root, "data_samples", "graphiti_semantic_mapping.json")
OUTPUT_TXT_PATH = os.path.join(project_root, "data_samples", "metadata.txt") # Menyimpan di data_samples

def convert_json_to_text_metadata(json_file_path: str, txt_file_path: str):
    """
    Mengonversi file graphiti_semantic_mapping.json menjadi format teks ringkas.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            semantic_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File JSON tidak ditemukan di {json_file_path}", file=sys.stderr)
        return
    except json.JSONDecodeError:
        print(f"ERROR: Gagal mem-parse JSON dari {json_file_path}", file=sys.stderr)
        return

    output_lines = ["SEMANTIC_METADATA_REPORT\n\n"]

    for table_name, table_details in semantic_data.items():
        output_lines.append(f"TABLE: {table_name}\n")
        
        purpose = table_details.get("purpose")
        if purpose:
            output_lines.append(f"  PURPOSE: {purpose}\n")
        
        category = table_details.get("business_category")
        if category:
            output_lines.append(f"  CATEGORY: {category}\n")
            
        output_lines.append("  COLUMNS:\n")
        columns_data = table_details.get("columns", {})
        if columns_data:
            for col_name, col_details in columns_data.items():
                line = f"    - NAME: {col_name}"
                
                col_type_db = col_details.get("type_from_db")
                if col_type_db:
                    line += f", TYPE_DB: {col_type_db}"

                col_desc = col_details.get("description")
                if col_desc:
                    line += f", DESC: {col_desc}"
                
                col_class = col_details.get("classification")
                if col_class:
                    line += f", CLASS: {col_class}"
                
                col_agg = col_details.get("is_aggregatable")
                if col_agg is not None: # Bisa False
                    line += f", AGGREGATABLE: {'Yes' if col_agg else 'No'}"
                
                output_lines.append(line + "\n")
        else:
            output_lines.append("    (No column details)\n")
            
        relationships = table_details.get("relationships", [])
        if relationships:
            output_lines.append("  RELATIONSHIPS:\n")
            for rel in relationships:
                from_col = rel.get("from_column")
                to_table = rel.get("to_table")
                to_col = rel.get("to_column")
                rel_type = rel.get("relationship_type", "FOREIGN_KEY") # Default jika tidak ada
                output_lines.append(f"    - FROM_COLUMN: {from_col}, TO_TABLE: {to_table}, TO_COLUMN: {to_col}, TYPE: {rel_type}\n")
        else:
            output_lines.append("  RELATIONSHIPS: (None specified or N/A)\n")
            
        output_lines.append("---\n") # Pemisah antar tabel

    try:
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.writelines(output_lines)
        print(f"Berhasil mengonversi metadata semantik ke {txt_file_path}")
    except IOError:
        print(f"ERROR: Gagal menulis ke file {txt_file_path}", file=sys.stderr)

if __name__ == "__main__":
    # Pastikan path INPUT_JSON_PATH dan OUTPUT_TXT_PATH sudah benar
    # relatif terhadap lokasi eksekusi skrip atau gunakan path absolut.
    # Jika skrip ini ada di folder 'scripts/', maka path di atas seharusnya sudah benar.
    
    print(f"Mencoba membaca dari: {INPUT_JSON_PATH}")
    print(f"Akan menulis ke: {OUTPUT_TXT_PATH}")
    
    convert_json_to_text_metadata(INPUT_JSON_PATH, OUTPUT_TXT_PATH)