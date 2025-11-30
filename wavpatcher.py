#!/usr/bin/env python3
"""
WavPatcher CLI - Convert WAV_EXTENSIBLE headers to standard PCM format.

This tool scans WAV files for WAV_EXTENSIBLE headers (format ID 65534) and
optionally patches them to standard PCM (format ID 1) for better compatibility
with certain audio equipment.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List


def patch_wav_files(
    directory: str,
    simulate: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Scan and optionally patch WAV files with extensible format headers.

    Parameters
    ----------
    directory : str
        Path to the directory containing WAV files (will search recursively)
    simulate : bool, default=True
        If True, only scan files without modifying them (dry-run mode)
        If False, patch files by replacing extensible headers
    verbose : bool, default=True
        If True, print detailed progress information

    Returns
    -------
    dict
        Dictionary containing results of the operation
    """
    total_files = 0
    extensible_files = 0
    patched_file_list: List[str] = []

    process_dir = Path(directory)
    if not process_dir.exists():
        return {
            'total_files': 0,
            'extensible_files': 0,
            'patched_files': [],
            'success': False,
            'error': f"Directory does not exist: {directory}"
        }

    wav_files = list(process_dir.rglob('*.wav'))
    total_files = len(wav_files)

    if total_files == 0:
        if verbose:
            print("No *.wav files could be found!")
        return {
            'total_files': 0,
            'extensible_files': 0,
            'patched_files': [],
            'success': True,
            'message': 'No WAV files found'
        }

    if verbose:
        mode_str = "DRY-RUN (scan only)" if simulate else "PATCH MODE"
        print(f"WavPatcher CLI - {mode_str}")
        print(f"Directory: {directory}")
        print(f"Total WAV files to scan: {total_files}\n")

    rwmode = "rb" if simulate else "rb+"

    for idx, path in enumerate(wav_files, 1):
        try:
            with open(path, rwmode) as f:
                f.seek(20, 0)
                format_id_bytes = f.read(2)
                format_id = int.from_bytes(format_id_bytes, byteorder='little', signed=False)

                if format_id == 65534:
                    extensible_files += 1
                    patched_file_list.append(str(path))

                    if verbose:
                        status = "[FOUND]" if simulate else "[PATCHED]"
                        print(f"{status} {path}")

                    if not simulate:
                        f.seek(-2, 1)
                        f.write(b'\x01\x00')

            if verbose and idx % 100 == 0:
                progress = (idx / total_files) * 100
                print(f"Progress: {progress:.1f}% ({idx}/{total_files})")

        except PermissionError:
            if verbose:
                print(f"[ERROR] Permission denied: {path}")
            continue
        except Exception as e:
            if verbose:
                print(f"[ERROR] {path}: {str(e)}")
            continue

    return {
        'total_files': total_files,
        'extensible_files': extensible_files,
        'patched_files': patched_file_list,
        'success': True
    }


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog='wavpatcher',
        description='Scan and patch WAV files with WAV_EXTENSIBLE headers to standard PCM format.',
        epilog='Example: python wavpatcher.py /path/to/music --patch'
    )

    parser.add_argument(
        'directory',
        type=str,
        help='Directory containing WAV files to process (searches recursively)'
    )

    parser.add_argument(
        '-p', '--patch',
        action='store_true',
        default=False,
        help='Actually patch files (default is dry-run/scan only)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=False,
        help='Suppress detailed output, only show summary'
    )

    parser.add_argument(
        '-l', '--list',
        action='store_true',
        default=False,
        help='List all files with extensible headers at the end'
    )

    args = parser.parse_args()

    # Validate directory
    if not Path(args.directory).exists():
        print(f"Error: Directory does not exist: {args.directory}", file=sys.stderr)
        return 1

    if not Path(args.directory).is_dir():
        print(f"Error: Path is not a directory: {args.directory}", file=sys.stderr)
        return 1

    # Run the patcher
    results = patch_wav_files(
        directory=args.directory,
        simulate=not args.patch,
        verbose=not args.quiet
    )

    if not results['success']:
        print(f"Error: {results.get('error', 'Unknown error')}", file=sys.stderr)
        return 1

    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total files scanned:      {results['total_files']}")
    print(f"Extensible headers found: {results['extensible_files']}")

    if args.patch and results['extensible_files'] > 0:
        print(f"Files patched:            {results['extensible_files']}")

    # List files if requested
    if args.list and results['extensible_files'] > 0:
        print("\nFiles with extensible headers:")
        for file_path in results['patched_files']:
            print(f"  {file_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
