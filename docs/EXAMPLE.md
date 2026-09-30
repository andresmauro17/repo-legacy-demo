# Worked Example: Modifying `legacy_code_upper()`

## Scenario
A developer modifies `app_legacy/models.py`, changing the logic of
`LegacyModel.legacy_code_upper()`.

## Step 1 — Developer triggers the check

```
> /check-blast-radius
```

## Step 2 — Claude queries `dependency-graph`

Request:
```json
{ "tool": "get_consumers", "arguments": { "symbol": "legacy_code_upper" } }
```

Response:
```json
{
  "symbol": "legacy_code_upper",
  "consumers": [
    { "repo": "reporting-service", "file": "reporting/exporters/csv_export.py", "line": 87, "relation": "direct_call" },
    { "repo": "sync-service", "file": "sync/handlers/oracle_sync.py", "line": 214, "relation": "direct_call" }
  ],
  "count": 2
}
```

## Step 3 — Claude queries `codebase-search`

Request:
```json
{ "tool": "search_code", "arguments": { "query": "usage of legacy_code_upper in sync-service", "top_k": 3 } }
```

Response:
```json
{
  "results": [
    {
      "repo": "sync-service",
      "file": "sync/handlers/oracle_sync.py",
      "lines": "210-218",
      "score": 0.91,
      "snippet": "def sync_record(record):\n    code = record.legacy_code_upper()\n    oracle_client.upsert(code, record.name)"
    }
  ]
}
```

## Step 4 — Final output in the developer's terminal

```
Blast radius: 2 of 3 dependent repos affected

reporting-service: legacy_code_upper() used in reporting/exporters/csv_export.py:87
  → The returned code is written directly into an exported CSV row;
    a format change here will silently corrupt exported reports.

sync-service: legacy_code_upper() used in sync/handlers/oracle_sync.py:214
  → The returned value is passed straight into oracle_client.upsert();
    if the format changes, the Oracle upsert may fail or write
    inconsistent records.

auth-gateway: no references found

Suggested: run reporting-service and sync-service test suites before
committing
  cd ../reporting-service && pytest tests/test_csv_export.py
  cd ../sync-service && pytest tests/test_oracle_sync.py
```