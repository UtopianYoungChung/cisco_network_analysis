#!/usr/bin/env python3
"""
Path utilities for accessing data directories in the cisco_network_analysis project.

This module provides functions to reliably get paths to data directories,
regardless of where the Python script or Jupyter notebook is running from.
"""

import os
from pathlib import Path


def get_project_root():
    """
    Get the absolute path to the project root directory.
    
    This function searches for the project root by looking for characteristic
    files/directories (like README.md, .git, etc.) starting from the current
    file's location and walking up the directory tree.
    
    Returns:
        Path: Absolute path to the project root directory.
        
    Raises:
        FileNotFoundError: If the project root cannot be determined.
    """
    # Start from the current file's directory
    current_path = Path(__file__).resolve().parent
    
    # Walk up the directory tree to find the project root
    for path in [current_path] + list(current_path.parents):
        # Check for characteristic files/directories
        # Look for README.md and optionally .git (may not exist in some deployments)
        has_readme = (path / 'README.md').exists()
        has_git = (path / '.git').exists()
        has_data_dir = (path / 'dir_g21_small_workload_with_gt').exists()
        
        # Consider it the project root if it has README.md and either .git or the data directory
        if has_readme and (has_git or has_data_dir):
            return path
    
    # Fallback: if we can't find the root, assume current file is in root
    return current_path


def get_g21_small_workload_path():
    """
    Get the absolute path to the dir_g21_small_workload_with_gt directory.
    
    This function returns the correct path to the g21 small workload directory
    regardless of where the calling code is located in the filesystem.
    
    Returns:
        str: Absolute path to dir_g21_small_workload_with_gt
        
    Raises:
        FileNotFoundError: If the directory does not exist.
        
    Example:
        >>> from path_utils import get_g21_small_workload_path
        >>> data_dir = get_g21_small_workload_path()
        >>> print(data_dir)
        /path/to/cisco_network_analysis/dir_g21_small_workload_with_gt
    """
    root = get_project_root()
    data_dir = root / 'dir_g21_small_workload_with_gt'
    
    if not data_dir.exists():
        raise FileNotFoundError(
            f"Directory not found: {data_dir}\n"
            f"Project root: {root}"
        )
    
    return str(data_dir)


def get_g21_subdirectory(subdir_name):
    """
    Get the absolute path to a subdirectory within dir_g21_small_workload_with_gt.
    
    Args:
        subdir_name (str): Name of the subdirectory (e.g., 'dir_no_packets_etc')
        
    Returns:
        str: Absolute path to the subdirectory
        
    Raises:
        FileNotFoundError: If the subdirectory does not exist.
        
    Example:
        >>> from path_utils import get_g21_subdirectory
        >>> subdir = get_g21_subdirectory('dir_no_packets_etc')
        >>> print(subdir)
        /path/to/cisco_network_analysis/dir_g21_small_workload_with_gt/dir_no_packets_etc
    """
    base_dir = Path(get_g21_small_workload_path())
    subdir = base_dir / subdir_name
    
    if not subdir.exists():
        raise FileNotFoundError(
            f"Subdirectory not found: {subdir}\n"
            f"Base directory: {base_dir}"
        )
    
    return str(subdir)


def get_g21_file_path(filename):
    """
    Get the absolute path to a file within dir_g21_small_workload_with_gt.
    
    Args:
        filename (str): Name of the file (e.g., 'groupings.gt.txt')
        
    Returns:
        str: Absolute path to the file
        
    Raises:
        FileNotFoundError: If the file does not exist.
        
    Example:
        >>> from path_utils import get_g21_file_path
        >>> gt_file = get_g21_file_path('groupings.gt.txt')
        >>> print(gt_file)
        /path/to/cisco_network_analysis/dir_g21_small_workload_with_gt/groupings.gt.txt
    """
    base_dir = Path(get_g21_small_workload_path())
    file_path = base_dir / filename
    
    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}\n"
            f"Base directory: {base_dir}"
        )
    
    return str(file_path)


if __name__ == '__main__':
    # Test the functions
    print("Testing path_utils.py")
    print("-" * 60)
    
    try:
        root = get_project_root()
        print(f"✓ Project root: {root}")
    except FileNotFoundError as e:
        print(f"✗ Error finding project root: {e}")
    
    try:
        g21_path = get_g21_small_workload_path()
        print(f"✓ G21 small workload path: {g21_path}")
    except FileNotFoundError as e:
        print(f"✗ Error finding G21 directory: {e}")
    
    try:
        subdir = get_g21_subdirectory('dir_no_packets_etc')
        print(f"✓ Subdirectory path: {subdir}")
    except FileNotFoundError as e:
        print(f"✗ Error finding subdirectory: {e}")
    
    try:
        gt_file = get_g21_file_path('groupings.gt.txt')
        print(f"✓ Ground truth file path: {gt_file}")
    except FileNotFoundError as e:
        print(f"✗ Error finding file: {e}")
    
    print("-" * 60)
    print("All tests passed!")
