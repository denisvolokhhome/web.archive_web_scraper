# Web Archive Email and Phone Extractor

This Python script extracts emails and phone numbers from archived web pages using the Wayback Machine (Internet Archive). It takes a list of URLs from a text file, retrieves archived versions of these URLs, and searches for emails and phone numbers on those pages. The results are saved in a CSV file.

## Requirements

Make sure you have Python installed. The required Python packages are listed in the `requirements.txt` file.

### Required Packages

- `requests`
- `beautifulsoup4`

You can install the required packages using:

```bash
pip install -r requirements.txt
```

## Usage

1. **Prepare a list of URLs**: Create a text file named `urls.txt` in the same directory as the script. List each URL on a new line.

   Example `urls.txt`:

   ```
   https://example.com
   https://another-example.com
   ```

2. **Run the script**:

   Execute the script using Python:

   ```bash
   python script_name.py
   ```

   Replace `script_name.py` with the actual name of your script file.

3. **Check the output**: The script will generate an `output.csv` file containing the URLs, extracted emails, and phone numbers.

## Output

The output will be a CSV file named `output.csv` with the following columns:

- `URL`: The original URL processed.
- `Emails`: A comma-separated list of extracted emails.
- `Phones`: A comma-separated list of extracted phone numbers.

## Error Handling

The script uses a retry strategy to handle network errors, timeouts, and specific HTTP status codes (e.g., 429, 500, 502, 503, 504). If an error occurs while fetching data, it will print an error message and continue processing the next URL.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to fork the repository, create a branch, and submit a pull request if you'd like to contribute to the project.

## Contact

For any questions or issues, please open an issue in the repository or contact the maintainer directly.
