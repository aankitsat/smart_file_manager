import os

# Ensure the folder exists
os.makedirs("samples", exist_ok=True)

# Create file1.txt
with open("samples/file1.txt", "w") as f:
    f.write("Hello World\nThis is a test file.")

# Create file2.txt
with open("samples/file2.txt", "w") as f:
    f.write("This is a different file content.")

# Create file1_copy.txt (same content as file1.txt)
with open("samples/file1_copy.txt", "w") as f:
    f.write("Hello World\nThis is a test file.")

print("✅ Sample files created successfully.")
