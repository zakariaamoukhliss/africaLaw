# Uploading the documents to Cloudflare R2

Expected result: **1,656 objects, 3,104,680,837 bytes (~2.89 GB)** in bucket `africa-laws-files`.
(Well under the R2 free tier of 10 GB storage.)

Files you need (kept **outside** this repo, next to your backup):
- `r2_upload_list.txt` - the 1,656 relative paths to upload (one per line, forward slashes)
- `r2_upload_manifest.csv` - path, size, sha256, whether the site links to it

`<BACKUP_DIR>` below = the extracted cPanel backup folder (the one that contains `Algeria\`, `Benin\`, `contracts\`, ...).

## 1. Install rclone and create the bucket

```powershell
winget install Rclone.Rclone
```

Cloudflare dashboard -> **R2 -> Create bucket** -> name `africa-laws-files`.
Then **R2 -> Manage R2 API Tokens -> Create API token** (permission: *Object Read & Write*, scoped to that bucket). Keep the Access Key ID / Secret to yourself; never commit them.

## 2. Configure rclone for this session only (nothing is written to disk)

```powershell
$env:RCLONE_CONFIG_R2_TYPE = "s3"
$env:RCLONE_CONFIG_R2_PROVIDER = "Cloudflare"
$env:RCLONE_CONFIG_R2_ACCESS_KEY_ID = "<ACCESS_KEY_ID>"
$env:RCLONE_CONFIG_R2_SECRET_ACCESS_KEY = "<SECRET_ACCESS_KEY>"
$env:RCLONE_CONFIG_R2_ENDPOINT = "https://<ACCOUNT_ID>.r2.cloudflarestorage.com"
$env:RCLONE_CONFIG_R2_ACL = "private"

rclone lsd r2:          # should list your buckets, including africa-laws-files
```

## 3. Dry run, then upload

`--files-from-raw` makes rclone upload **only** the listed documents (it will not touch the nested .tar/.zip backups, .sql dumps, mail or config files that sit in the same folder).

```powershell
rclone copy "<BACKUP_DIR>" r2:africa-laws-files --files-from-raw "<WORK_DIR>\r2_upload_list.txt" --dry-run -v

rclone copy "<BACKUP_DIR>" r2:africa-laws-files --files-from-raw "<WORK_DIR>\r2_upload_list.txt" `
  --transfers 16 --checkers 16 --s3-no-check-bucket --progress --log-file "<WORK_DIR>\r2_upload.log" --log-level INFO
```

The command is safe to re-run; it skips what is already uploaded.

## 4. Verify

```powershell
# every listed file exists remotely with the same size (and checksum where R2 provides one)
rclone check "<BACKUP_DIR>" r2:africa-laws-files --files-from-raw "<WORK_DIR>\r2_upload_list.txt" --one-way

# if check complains only about hashes of large multipart uploads, compare sizes:
rclone check "<BACKUP_DIR>" r2:africa-laws-files --files-from-raw "<WORK_DIR>\r2_upload_list.txt" --one-way --size-only

# strictest (downloads everything again, ~2.9 GB): byte-for-byte
rclone check "<BACKUP_DIR>" r2:africa-laws-files --files-from-raw "<WORK_DIR>\r2_upload_list.txt" --one-way --download

# final count + total size: must print 1656 objects and 3104680837 bytes
rclone size r2:africa-laws-files
(rclone lsf r2:africa-laws-files --files-only -R | Measure-Object -Line).Lines     # 1656
```

## 5. Serve the bucket at files.africa-laws.org

R2 -> `africa-laws-files` -> **Settings -> Custom Domains -> Add** `files.africa-laws.org`
(the domain's DNS must be on the same Cloudflare account). Then spot-check, for example:

```
https://files.africa-laws.org/contracts/NDA/NDA.docx
https://files.africa-laws.org/Morocco/banking%20and%20finance%20law/Loi%20bancaire-%202014.pdf
```

Do **not** enable the public `r2.dev` URL for production.
