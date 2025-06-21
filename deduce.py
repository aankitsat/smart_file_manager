import hashlib
import os

TABLE_SIZE = 1000

class DuplicateRemover:
    def __init__(self):
        self.hash_table = [None] * TABLE_SIZE
        self.deleted_files = []

    def compute_sha256(self, file_path):
        """Compute SHA-256 hash of a file's content."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(4096):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return None

    def _hash_index(self, sha_hash):
        return int(sha_hash, 16) % TABLE_SIZE

    def insert_or_delete(self, file_info):
        sha_hash = self.compute_sha256(file_info['path'])
        if not sha_hash:
            print(f"File not found: {file_info['path']}")
            return

        index = self._hash_index(sha_hash)
        start_index = index

        while self.hash_table[index] is not None:
            # If duplicate found
            if self.hash_table[index][0] == sha_hash:
                print(f"❌ Duplicate found: {file_info['name']} -> Deleting")
                try:
                    os.remove(file_info['path'])
                    self.deleted_files.append(file_info['name'])
                except Exception as e:
                    print(f"Error deleting {file_info['name']}: {e}")
                return

            index = (index + 1) % TABLE_SIZE
            if index == start_index:
                raise Exception("Hash table full")

        # No duplicate: insert
        self.hash_table[index] = (sha_hash, file_info)
        print(f"✅ Kept: {file_info['name']}")

    def summary(self):
        print("\n=== Deletion Summary ===")
        if self.deleted_files:
            for name in self.deleted_files:
                print(f"- {name}")
        else:
            print("No duplicates found.")

# 🔽 Example usage
if __name__ == "__main__":
    files = [
        {"name": "file1.txt", "path": "samples/file1.txt"},
        {"name": "file2.txt", "path": "samples/file2.txt"},
        {"name": "file1_copy.txt", "path": "samples/file1_copy.txt"}
    ]

    remover = DuplicateRemover()
    for f in files:
        remover.insert_or_delete(f)

    remover.summary()
