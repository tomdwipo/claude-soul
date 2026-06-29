---
name: fig-decode
description: Decode a Figma `.fig` file (format v100+) into a structured JSON node tree so questions like "what's at node 52502:42168?" can be answered without opening Figma. Useful for design auditing, Figma→Compose traceability, and PRD/Figma cross-checks when the design lives only as a `.fig` export.
metadata:
  author: Tommy Dwi
  keywords:
  - figma
  - fig-kiwi
  - kiwi-schema
  - design-system
  - figma-decode
  - figma-node
  - node-id
---

## When to use

Invoke this skill when a user:

- Provides a path to a `.fig` file on disk and asks to "look inside" / "explain" / "list pages" / "find a screen".
- Pastes a Figma URL like `https://www.figma.com/design/<file-key>/...?node-id=NNNN-NNNN` **and** the corresponding `.fig` is available locally — translate the URL's `node-id` to `NNNN:NNNN` (replace `-` with `:`) and look it up.
- Asks "which screen in code corresponds to Figma node X?" — combine the decoded structure with a grep over the codebase.

**Do not** invoke this skill if the file is only accessible via the Figma cloud — use `mcp__figma__*` tools for those (they need an API token and the file's cloud URL).

## Requirements

The decoder runs entirely locally:

- `node` 18+ (uses `npm install` to fetch `kiwi-schema` and `pako` on first run)
- `zstd` CLI (`brew install zstd` on macOS — Figma `.fig` v100+ uses zstd for the document payload)
- `unzip` (system-default)

## How to invoke

The pipeline lives at `.docs/tools/fig-decode/`. From repo root:

```bash
.docs/tools/fig-decode/decode.sh "/path/to/file.fig"
# → prints the output directory it wrote to, defaults to $TMPDIR/fig-decode-<basename>
```

Pass `--full` if the user wants the entire decoded message tree (large — every NodeChange with all 590 fields). Default mode writes only the lightweight `nodes-summary.json` (one record per NodeChange: `{guid, parent, type, name, phase}`).

## How a node-id maps to the output

Figma URLs encode node ids as `NNNN-NNNN`. The same id appears in the decoded tree as a GUID `{sessionID: NNNN, localID: NNNN}`. Use the helper:

```bash
.docs/tools/fig-decode/scripts/find_node.py 52502-42168
# → prints the matched node, its parent chain back to the canvas/document, and direct children
```

Without `--out`, the helper picks the most recently decoded `fig-decode-*` directory in `$TMPDIR`.

## Pipeline outputs

```
$TMPDIR/fig-decode-<basename>/
├── canvas.fig          inner Kiwi binary (unzipped from outer .fig archive)
├── meta.json           outer archive metadata
├── thumbnail.png       embedded preview
├── images/             bundled raster assets the design references
├── schema.bin          DEFLATE-decompressed Kiwi schema chunk
├── schema.txt          human-readable schema (`prettyPrintSchema` output)
├── document.bin        zstd-decompressed Kiwi message stream
├── nodes-summary.json  [{guid, parent, type, name, phase}] for every NodeChange
├── stats.json          message/node counts, type histogram, page names
└── message-full.json   only with --full (large)
```

## What the user can do with the output

- **Find a node**: `scripts/find_node.py NODE-ID` (URL form or colon form both work).
- **Inspect a section**: open `nodes-summary.json` and walk children of any GUID. Each NodeChange's `parent` is a `{sessionID, localID}` matching a GUID in the same file.
- **List pages**: read `stats.json` → `pageNames`. Pages are CANVAS-type nodes.
- **Schema introspection**: `schema.txt` lists all 605 Figma message types and their field IDs — useful when extending the walker to extract additional properties (fills, strokes, geometry).

## Format notes (what the decoder handles)

The outer `.fig` is a ZIP archive. Inside is `canvas.fig`, which is Kiwi-encoded binary with this layout:

```
magic           "fig-kiwi"  (8 bytes)
version         uint32 LE   (format version; this repo's files are v106)
chunk[0]        uint32 length + payload   (Kiwi schema, DEFLATE-compressed)
chunk[1]        uint32 length + payload   (document, zstd-compressed in v100+)
```

The community `fig-kiwi@0.0.1` npm package is **not** compatible with v100+ files (it expects DEFLATE for both chunks). The decoder here detects compression per-chunk and uses `zstd` CLI for the document stream. Chunk[1] is a *stream* of `Message` records, not one — iterate `compiled.decodeMessage(bb)` until the buffer is exhausted.

## Limits

- The decoder does not (yet) extract pixel-level visual properties (positions, fills, strokes, fonts). `nodes-summary.json` is the **structural** tree only. To get visual properties, extend the walker to capture more fields from each `NodeChange` per `schema.txt`.
- Decoded message tree is ~5-10× the size of the original `.fig` — a 250 MB `.fig` produces a 1+ GB JSON if `--full` is passed. Output goes to `$TMPDIR` by default; pass `--out=` to redirect.
- Re-running on the same `.fig` overwrites the same `$TMPDIR/fig-decode-<basename>/` (idempotent).
