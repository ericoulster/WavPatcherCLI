# WavPatcher CLI

A command-line fork of [WavPatcher](https://github.com/ckbaudio/wavpatcher) designed to scan and patch WAV files with WAV_EXTENSIBLE headers (format ID 65534) to standard PCM format (format ID 1) for better compatibility with audio equipment.

This fork was built to easily solve Linux compatibility and for people who are more comfortable with the command line than GUI tools.

## Requirements

Python 3.6+

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

## What is WAV_EXTENSIBLE?

[WAV_EXTENSIBLE](https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/ksmedia/ns-ksmedia-waveformatextensible) (format ID 65534 / 0xFFFE) is an extension to the RIFF/WAV header which allows for custom or pre-defined channel-to-speaker mappings among other things. While it's a valid format, some older audio equipment and software don't recognize it properly.

Some services and software write WAV_EXT to generate WAV files from raw PCM or rendered audio if the file uses above CD-quality standards. While this is technically best practice, it isn't totally necessary for stereo files in most cases. As a result, generic WAV files that use the ext flag can become unsupported by standalone media equipment even if the quality attributes of the file are otherwise compatible.

This tool converts the format ID from 65534 (extensible) to 1 (standard PCM), which improves compatibility while preserving the audio data.

## Why Use WavPatcher?

- There isn't any easy or automated way to know whether WAV_EXT flags are present without a verbose metadata reader
- Large libraries of WAV files make it laborious to manually identify this problem
- This tool doesn't do any form of encoding and only touches files that exhibit the EXT header flag
- Faster than batch transcoding and requires less resources
- Particularly useful for DJs as patching libraries won't break files or require re-importing/re-analysing

## Limitations

- **Not an encoder/converter**: If your audio system does not support playback of files beyond 48kHz/24-bit, this tool will not make them supported. Use transcoding software for that.
- **Destructive**: There is no 'undo' function and files are written directly on-disk. Use dry-run mode (default) first to check your library before patching.

**Use this tool at your own risk.**

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid directory, permission issues, etc.) |

## About

This is a CLI fork of the original [WavPatcher](https://github.com/ckbaudio/wavpatcher) by ckbaudio.

I adapted this for personal use, but feel free to fork, edit and further iterate as needed.