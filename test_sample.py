#!/usr/bin/env python3
"""Tests for the path_utils module."""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from path_utils import (
    get_project_root,
    get_g21_small_workload_path,
    get_g21_subdirectory,
    get_g21_file_path
)


def test_get_project_root():
    """Test that get_project_root returns a valid directory."""
    root = get_project_root()
    assert Path(root).exists(), f"Project root does not exist: {root}"
    assert (Path(root) / 'README.md').exists(), "README.md not found in project root"
    print("✓ test_get_project_root passed")


def test_get_g21_small_workload_path():
    """Test that get_g21_small_workload_path returns a valid directory."""
    data_dir = get_g21_small_workload_path()
    assert os.path.exists(data_dir), f"Data directory does not exist: {data_dir}"
    assert os.path.isdir(data_dir), f"Path is not a directory: {data_dir}"
    assert 'dir_g21_small_workload_with_gt' in data_dir, "Path does not contain expected directory name"
    print("✓ test_get_g21_small_workload_path passed")


def test_get_g21_subdirectory():
    """Test that get_g21_subdirectory returns a valid subdirectory."""
    subdir = get_g21_subdirectory('dir_no_packets_etc')
    assert os.path.exists(subdir), f"Subdirectory does not exist: {subdir}"
    assert os.path.isdir(subdir), f"Path is not a directory: {subdir}"
    assert subdir.endswith('dir_no_packets_etc'), "Subdirectory path is incorrect"
    print("✓ test_get_g21_subdirectory passed")


def test_get_g21_file_path():
    """Test that get_g21_file_path returns a valid file path."""
    file_path = get_g21_file_path('groupings.gt.txt')
    assert os.path.exists(file_path), f"File does not exist: {file_path}"
    assert os.path.isfile(file_path), f"Path is not a file: {file_path}"
    assert file_path.endswith('groupings.gt.txt'), "File path is incorrect"
    print("✓ test_get_g21_file_path passed")


def test_all_paths_are_absolute():
    """Test that all returned paths are absolute."""
    root = get_project_root()
    assert os.path.isabs(str(root)), "Project root path is not absolute"
    
    data_dir = get_g21_small_workload_path()
    assert os.path.isabs(data_dir), "Data directory path is not absolute"
    
    subdir = get_g21_subdirectory('dir_no_packets_etc')
    assert os.path.isabs(subdir), "Subdirectory path is not absolute"
    
    file_path = get_g21_file_path('groupings.gt.txt')
    assert os.path.isabs(file_path), "File path is not absolute"
    
    print("✓ test_all_paths_are_absolute passed")


def test_example():
    """Original test example."""
    assert 1 + 1 == 2
    print("✓ test_example passed")


if __name__ == '__main__':
    print("Running path_utils tests...")
    print("-" * 60)
    
    test_example()
    test_get_project_root()
    test_get_g21_small_workload_path()
    test_get_g21_subdirectory()
    test_get_g21_file_path()
    test_all_paths_are_absolute()
    
    print("-" * 60)
    print("All tests passed!")

