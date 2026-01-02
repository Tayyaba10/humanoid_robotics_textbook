#!/usr/bin/env python3
"""
Comprehensive test suite runner for Qdrant RAG Retrieval Pipeline Validation.
This script runs all tests in the appropriate order and reports results.
"""

import subprocess
import sys
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, description, cwd=None):
    """
    Run a command and return the result.

    Args:
        cmd: Command to run as a list of strings
        description: Description of what the command does
        cwd: Working directory to run the command in

    Returns:
        tuple: (success: bool, output: str, error: str)
    """
    logger.info(f"Running: {description}")
    logger.info(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=300  # 5 minute timeout
        )
        success = result.returncode == 0
        logger.info(f"Command {'succeeded' if success else 'failed'} with return code {result.returncode}")
        if result.stdout:
            logger.debug(f"STDOUT: {result.stdout}")
        if result.stderr:
            logger.debug(f"STDERR: {result.stderr}")
        return success, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after 5 minutes: {' '.join(cmd)}")
        return False, "", "Command timed out"
    except Exception as e:
        logger.error(f"Error running command: {e}")
        return False, "", str(e)

def run_unit_tests():
    """Run unit tests"""
    logger.info("Running unit tests...")
    success, _, _ = run_command([
        sys.executable, "-m", "pytest",
        "backend/tests/unit/",
        "-v",
        "--tb=short"
    ], "Unit tests")
    return success

def run_integration_tests():
    """Run integration tests"""
    logger.info("Running integration tests...")
    success, _, _ = run_command([
        sys.executable, "-m", "pytest",
        "backend/tests/integration/",
        "-v",
        "--tb=short"
    ], "Integration tests")
    return success

def run_contract_tests():
    """Run contract tests"""
    logger.info("Running contract tests...")
    success, _, _ = run_command([
        sys.executable, "-m", "pytest",
        "backend/tests/contract/",
        "-v",
        "--tb=short"
    ], "Contract tests")
    return success

def run_performance_tests():
    """Run performance tests"""
    logger.info("Running performance tests...")
    success, _, _ = run_command([
        sys.executable, "-m", "pytest",
        "backend/tests/performance/",
        "-v",
        "--tb=short"
    ], "Performance tests")
    return success

def run_all_tests():
    """Run all test suites in order"""
    logger.info("Starting comprehensive test suite...")

    results = {}

    # Run unit tests first
    results['unit'] = run_unit_tests()
    if not results['unit']:
        logger.error("Unit tests failed, stopping execution")
        return False

    # Run integration tests
    results['integration'] = run_integration_tests()

    # Run contract tests
    results['contract'] = run_contract_tests()

    # Run performance tests
    results['performance'] = run_performance_tests()

    # Report results
    logger.info("\n" + "="*50)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("="*50)

    all_passed = True
    for test_type, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        logger.info(f"{test_type.capitalize():<12}: {status}")
        if not passed:
            all_passed = False

    logger.info("="*50)
    logger.info(f"Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    logger.info("="*50)

    return all_passed

def check_prerequisites():
    """Check if all prerequisites are met"""
    logger.info("Checking prerequisites...")

    # Check if pytest is available
    try:
        import pytest
        logger.info(f"✓ pytest version {pytest.__version__} is available")
    except ImportError:
        logger.error("✗ pytest is not installed")
        return False

    # Check if required directories exist
    required_dirs = [
        "backend/tests/unit",
        "backend/tests/integration",
        "backend/tests/contract",
        "backend/tests/performance"
    ]

    all_dirs_exist = True
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            logger.warning(f"Directory does not exist: {dir_path}")
            all_dirs_exist = False

    if all_dirs_exist:
        logger.info("✓ All test directories exist")
    else:
        logger.info("Note: Some test directories may not exist yet")

    # Check if backend directory exists
    if not os.path.exists("backend"):
        logger.error("✗ backend directory does not exist")
        return False

    logger.info("✓ Prerequisites check completed")
    return True

def main():
    """Main entry point for the test suite runner."""
    logger.info("Qdrant RAG Retrieval Pipeline - Comprehensive Test Suite")
    logger.info("="*60)

    # Check prerequisites
    if not check_prerequisites():
        logger.error("Prerequisites check failed, exiting...")
        return 1

    # Run all tests
    all_tests_passed = run_all_tests()

    # Exit with appropriate code
    if all_tests_passed:
        logger.info("\n🎉 All tests completed successfully!")
        return 0
    else:
        logger.error("\n❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())