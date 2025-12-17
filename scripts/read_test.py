#!/usr/bin/env python3
"""
Read/download file from GCS and publish event to Kafka
"""
import sys
import os
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from services.gcs_service import GCSService

def test_file_read():
    """Test reading files from GCS"""
    
    try:
        # Initialize GCS service with Kafka enabled
        gcs = GCSService(enable_kafka=True)
        
        # File to read
        filename = "uploads/sample.txt"
        
        print("=" * 50)
        print("GCS File Read Operations with Kafka Events")
        print("=" * 50)
        
        # 1. Check if file exists
        print(f"\n1. Checking if file exists: {filename}")
        files = gcs.list_files(prefix=filename)
        
        if filename not in files and not any(f.startswith(filename) for f in files):
            print(f"❌ File not found: {filename}")
            print("   Please upload a file first using upload_test.py")
            return False
        
        print(f"✅ File found: {filename}")
        
        # 2. Download file
        print(f"\n2. 📥 Downloading file...")
        download_path = f"downloaded_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        result = gcs.read_file(
            gcs_path=filename,
            download_to=download_path
        )
        print(f"✅ {result}")
        
        # 3. Read file content directly
        print(f"\n3. 🔍 Reading content directly from GCS...")
        try:
            text = gcs.read_file_text(filename)
            print("File content:")
            print("-" * 40)
            print(text[:500])  # Show first 500 chars
            if len(text) > 500:
                print("... (truncated)")
            print("-" * 40)
        except Exception as e:
            print(f"⚠️  Could not read as text: {str(e)}")
            print("   File might be binary or have encoding issues")
        
        # 4. Show downloaded file info
        if os.path.exists(download_path):
            print(f"\n4. 📊 Downloaded file information:")
            print(f"   Path: {download_path}")
            print(f"   Size: {os.path.getsize(download_path)} bytes")
            print(f"   Modified: {datetime.fromtimestamp(os.path.getmtime(download_path))}")
        
        print(f"\n✅ All read operations completed!")
        print(f"📧 Read events have been published to Kafka")
        
        return True
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def list_available_files():
    """List all available files in GCS"""
    try:
        gcs = GCSService(enable_kafka=False)
        print("\n📂 Available files in GCS:")
        files = gcs.list_files(prefix="")
        
        if files:
            for file in files[:20]:  # Show first 20 files
                print(f"   - {file}")
            if len(files) > 20:
                print(f"   ... and {len(files) - 20} more files")
        else:
            print("   No files found in bucket")
            
    except Exception as e:
        print(f"❌ Failed to list files: {str(e)}")

if __name__ == "__main__":
    success = test_file_read()
    
    if not success:
        list_available_files()
    
    print("\n" + "=" * 50)
    print("Kafka events published for each read operation")
    print("=" * 50)