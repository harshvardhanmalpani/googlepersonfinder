<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/ImportCSV'>direct link</a>).</font>

Instead of using [XML-based write API](DataAPI.md), you can also use CSV import tool to import your data into a Person Finder repository if you maintain your data in a spreadsheet or other database that support CSV export. Visit the following URL with <font color='#a00'><i>repository</i></font> replaced with the repository ID to which you want to import your data.

> `https://www.google.org/personfinder/`<font color='#a00'><i>repository</i></font>`/api/import`

## How to import your data in CSV format ##
  * Download [the sample CSV file](http://google.org/personfinder/global/sample-import.csv), and open it in a spreadsheet software such as Microsoft Excel or Google Drive.
  * Delete the first sample record and replace with your own data.
  * When ready, export the spreadsheet to a CSV file, and upload the file from the CSV import page (see above for the URL).
  * You need to have an authentication key with write permission to import your data ([request here](https://support.google.com/personfinder/contact/pf_api?rd=1)).
  * Once the file is uploaded, you will see a report and optionally error messages why some records were not imported successfully.

## How to update your data that is already imported ##
  * As long as person\_record\_id and note\_record\_id do not change, you can always edit the CSV file that is already imported, and upload it on the import page. Records with the same record ID are overwritten with the new data.

## How to format CSV files for a successful import and a few tips ##
  * Each row corresponds to a Person record or Note record.
  * Optionally, a Person entry and a Note entry for the person may be combined into one row, in which case photo\_url field is associated with the Person entry only, and the rest of the fields with identical name are associated with both the Person and Note entries.
  * The first header row specifies what should be entered in each field. See [PFIF 1.4 specifications](http://zesty.ca/pfif/1.4/) for the description of each field. **Required fields** are person\_record\_id, source\_date, full\_name for a Person record, and note\_record\_id, person\_record\_id, author\_name, source\_date, text for a Note record. The order of columns does not matter.
  * person\_record\_id and note\_record\_id should not contain a slash, Person Finder automatically prefixes those IDs with the domain registered with your authentication key and a slash.
  * All dates and times must be in UTC and in the format yyyy-mm-ddThh:mm:ssZ (**TODO:ryok** update instruction here)
  * For more details, please refer to the [PFIF 1.4 specifications](http://zesty.ca/pfif/1.4/).