"""Script to extract structured data from documentation files"""
import sys
import os
sys.path.append('src')

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from extraction.extractor import DataExtractor
import config

def main():
    print("\n" + "="*60)
    print("📊 Data Extraction Script")
    print("="*60)
    print("\nThis script will:")
    print("1. Read all markdown files from configured paths")
    print("2. Use LLM to extract structured information")
    print("3. Save results to data/extracted_data.json")
    print("\n" + "="*60 + "\n")
    
    # Create extractor
    extractor = DataExtractor()
    
    # Extract from all documentation
    extracted_data = extractor.extract_all(config.DOCS_PATHS)
    
    # Save to JSON
    output_path = "data/extracted_data.json"
    extractor.save_to_json(extracted_data, output_path)
    
    print("\n✅ Done! You can now use the extracted data for structured queries.")
    print(f"📄 Data saved to: {output_path}\n")

if __name__ == "__main__":
    main()
