import csv, os

class RemoveHeader:
    """
    Remove the header from CSV files in the current directory.
    Combine these files into a new CSV file.
    """
    def __init__(self,
                 directory="remove_header", 
                 new_filename="remove_header.csv"):
        self._directory = directory
        self._filenames = self._get_filenames()
        self._new_filename = new_filename

    def _get_filenames(self):
        return sorted([os.path.join(self._directory, f) 
                for f in os.listdir(self._directory) if f.endswith(".csv")])


    def remove_headers(self):
        with open(self._new_filename, "w", newline="") as f:
            writer = csv.writer(f)
            for filename in self._filenames:
                rows = self._remove_header_from_file(filename)
                writer.writerows(rows)

    def _remove_header_from_file(self, filename):
        """
        Remove the header from CSV file and append its content to the new file.
        """
        with open(filename) as f:
            # Prit the filename
            print(f"Removing header from {filename}...")
            # Read the file and skip the header
            reader = csv.reader(f)
            rows = list(reader)[1:]
        return rows

if __name__ == "__main__":
    rh = RemoveHeader(directory="dummy_csv_files", 
                      new_filename="dummy_csv_files_combined.csv")
    print("Removing headers from CSV files...")
    rh.remove_headers()
    print("Done removing headers.")