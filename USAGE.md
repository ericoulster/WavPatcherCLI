# WavPatcher CLI

A command-line tool to scan and patch WAV files with WAV_EXTENSIBLE headers (format ID 65534) to standard PCM format (format ID 1) for better compatibility with audio equipment.

## Installation

No installation required. Just ensure you have Python 3.6+ installed.

```bash
# Make the script executable (optional)
chmod +x wavpatcher.py
```

## Usage

```bash
python wavpatcher.py <directory> [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `directory` | Path to the directory containing WAV files (searches recursively) |

### Options

| Option | Description |
|--------|-------------|
| `-p, --patch` | Actually patch the files. Without this flag, the tool runs in dry-run mode (scan only) |
| `-q, --quiet` | Suppress detailed output, only show the summary |
| `-l, --list` | List all files with extensible headers at the end of output |
| `-h, --help` | Show help message |

## Examples

### Scan files (dry-run mode)

Scan a directory to find WAV files with extensible headers without modifying anything:

```bash
python wavpatcher.py /path/to/music
```

### Patch files

Scan and patch all WAV files with extensible headers:

```bash
python wavpatcher.py /path/to/music --patch
```

### Quiet mode with file listing

Run quietly and list affected files at the end:

```bash
python wavpatcher.py /path/to/music --quiet --list
```

### Patch with file listing

Patch files and show which ones were modified:

```bash
python wavpatcher.py /path/to/music -p -l
```

## Output

### Dry-run mode (default)

```
WavPatcher CLI - DRY-RUN (scan only)
Directory: /path/to/music
Total WAV files to scan: 150

[FOUND] /path/to/music/track1.wav
[FOUND] /path/to/music/subfolder/track2.wav

==================================================
SUMMARY
==================================================
Total files scanned:      150
Extensible headers found: 2
```

### Patch mode

```
WavPatcher CLI - PATCH MODE
Directory: /path/to/music
Total WAV files to scan: 150

[PATCHED] /path/to/music/track1.wav
[PATCHED] /path/to/music/subfolder/track2.wav

==================================================
SUMMARY
==================================================
Total files scanned:      150
Extensible headers found: 2
Files patched:            2
```

## What is WAV_EXTENSIBLE?

WAV_EXTENSIBLE (format ID 65534 / 0xFFFE) is an extended WAV format that supports additional metadata like channel masks and sub-formats. While it's a valid format, some older audio equipment and software don't recognize it properly.

This tool converts the format ID from 65534 (extensible) to 1 (standard PCM), which improves compatibility while preserving the audio data.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid directory, permission issues, etc.) |
