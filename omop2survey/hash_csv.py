import hashlib
import os


def hash_csv(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


if __name__ == "__main__":
    csv_file_path = 'omop2survey/survey_key.csv'

    file_hash = hash_csv(csv_file_path)

    hash_file_path = os.path.splitext(csv_file_path)[0] + '_hash.txt'
    with open(hash_file_path, 'w') as f:
        f.write(file_hash)

    print(f"The hash of the file {csv_file_path} is: {file_hash}")
    print(f"Hash saved to: {hash_file_path}")
