#!/usr/bin/env python3
"""Test the utils package"""

from datetime import datetime, timedelta
from utils.helpers import format_date, format_datetime, time_ago
from utils.validators import validate_email, validate_phone, validate_url, validate_password
from utils.constants import (
    HTTP_OK, ROLE_ADMIN, TASK_PENDING, DATE_FORMAT_SHORT,
    ERROR_INVALID_EMAIL, SUCCESS_LOGIN
)

print("=" * 60)
print("Testing Utils Package")
print("=" * 60)

# Test 1: Helpers - Date Formatting
print("\n[TEST 1] Date Formatting")
print("-" * 60)
test_date = datetime(2026, 6, 2)
print(f"format_date: {format_date(test_date)}")
print(f"format_datetime: {format_datetime(test_date)}")
print(f"time_ago (few seconds): {time_ago(datetime.now() - timedelta(seconds=30))}")
print(f"time_ago (2 hours): {time_ago(datetime.now() - timedelta(hours=2))}")
print(f"time_ago (5 days): {time_ago(datetime.now() - timedelta(days=5))}")

# Test 2: Validators - Email
print("\n[TEST 2] Email Validation")
print("-" * 60)
test_emails = [
    "tanvir0102@gmail.com",
    "invalid.email@",
    "user@example.co.uk",
    "not-an-email"
]
for email in test_emails:
    result = validate_email(email)
    status = "VALID" if result else "INVALID"
    print(f"{email:<25} -> {status}")

# Test 3: Validators - Phone
print("\n[TEST 3] Phone Validation")
print("-" * 60)
test_phones = [
    "123-456-7890",
    "(123) 456-7890",
    "+1 123 456 7890",
    "123456",
    "123-456"
]
for phone in test_phones:
    result = validate_phone(phone)
    status = "VALID" if result else "INVALID"
    print(f"{phone:<25} -> {status}")

# Test 4: Validators - URL
print("\n[TEST 4] URL Validation")
print("-" * 60)
test_urls = [
    "https://example.com",
    "http://google.com/search",
    "invalid-url",
    "ftp://example.com"
]
for url in test_urls:
    result = validate_url(url)
    status = "VALID" if result else "INVALID"
    print(f"{url:<35} -> {status}")

# Test 5: Validators - Password Strength
print("\n[TEST 5] Password Strength Validation")
print("-" * 60)
test_passwords = [
    "weak",
    "WeakPass123",
    "StrongPass123!",
    "MyP@ssw0rd"
]
for pwd in test_passwords:
    result = validate_password(pwd)
    status = "VALID" if result['valid'] else "INVALID"
    print(f"\nPassword: {pwd}")
    print(f"Status: {status}")
    if result['errors']:
        for error in result['errors']:
            print(f"  - {error}")

# Test 6: Constants Usage
print("\n[TEST 6] Constants")
print("-" * 60)
print(f"HTTP_OK status code: {HTTP_OK}")
print(f"Admin role: {ROLE_ADMIN}")
print(f"Pending task status: {TASK_PENDING}")
print(f"Date format short: {DATE_FORMAT_SHORT}")
print(f"Error message: {ERROR_INVALID_EMAIL}")
print(f"Success message: {SUCCESS_LOGIN}")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)
