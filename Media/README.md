# Media report extract

Download project photos through the Documents V2 API and generate an Excel index with relative links to each photo.

## Setup

Use Python 3.10 or later. From this folder, install the dependencies:

```sh
python -m pip install -r requirements.txt
```

Edit `media_extract.settings.json`:

- `baseUrl`: Media API root URL, including the Media API path when using a gateway. The supplied default is `http://localhost:5005` for local development.
- `filter`: `{}` for all project photos, or use `space` (`Area`, `Item`, `Issue`) and/or `areaIdPrefix`.
- `outputPath`: Output folder, relative to this script unless absolute. Supports `{timestamp}`.
- `outputFileName`: Optional ZIP filename; defaults to `media-extract-{timestamp}.zip`.
- `pageSize`: Metadata page size, up to 10000.
- `progressEvery`: Log progress every N photos.

For example, to extract item photos within an area-number prefix:

```json
"filter": { "space": "Item", "areaIdPrefix": "1.2" }
```

## Run

Set the `Ocp-Apim-Subscription-Key` environment variable to your subscription key, then run:

```sh
python media_client_extract.py
```

Alternatively, pass the key as the first argument:

```sh
python media_client_extract.py <subscription-key>
```

Keep subscription keys out of committed files.

## API prerequisites

The configured API must expose `POST /v2/Documents/metadata` and `GET /v2/Documents/{mediaId}/file`. If using APIM, these operations must be imported and routed to the Media backend.

The script also checks `GET /swagger/v1/swagger.json` without a subscription key before starting. That URL must be accessible and its document title must contain `AssetFuture.API.Media`; a gateway exposing only the document operations will fail this check.

## Output

- `photos/`: Downloaded photos, using the relative paths supplied by the API.
- `index.xlsx`: Type, area ID/path, item/issue IDs, title, filename, and photo links.
- `unmapped-areas.csv`: Unmapped media identifiers, created only when unmapped records exist.
- `metadata.json`: Retrieved metadata, retained in the output folder.
- `media-extract-<timestamp>.zip`: Photos, Excel index, and the unmapped CSV when present. The ZIP does not include `metadata.json`.

Extract the ZIP before opening the index so its relative photo links work.
