#!/usr/bin/env python3
"""Test the task manager app functionality"""

import json
import os

# Test 1: Verify all files exist
print("=" * 50)
print("TEST 1: File Existence")
print("=" * 50)

files = ['index.html', 'style.css', 'app.js']
for file in files:
    exists = os.path.exists(file)
    status = "[PASS]" if exists else "[FAIL]"
    print(f"{status}: {file}")

# Test 2: Verify HTML structure
print("\n" + "=" * 50)
print("TEST 2: HTML Structure")
print("=" * 50)

with open('index.html', 'r') as f:
    html_content = f.read()

required_elements = [
    ('taskInput', 'input field for new tasks'),
    ('addBtn', 'add task button'),
    ('taskList', 'task list container'),
    ('totalCount', 'total task counter'),
    ('completedCount', 'completed task counter')
]

for element_id, description in required_elements:
    has_element = f'id="{element_id}"' in html_content
    status = "[PASS]" if has_element else "[FAIL]"
    print(f"{status}: {description} (id: {element_id})")

# Test 3: Verify CSS file has styling
print("\n" + "=" * 50)
print("TEST 3: CSS Styling")
print("=" * 50)

with open('style.css', 'r') as f:
    css_content = f.read()

css_classes = [
    ('container', 'main container'),
    ('input-section', 'input section'),
    ('task-list', 'task list'),
    ('task-item', 'task item styling'),
    ('delete-btn', 'delete button'),
    ('task-text', 'task text'),
    ('.completed', 'completed task styling')
]

for class_name, description in css_classes:
    has_class = class_name in css_content
    status = "[PASS]" if has_class else "[FAIL]"
    print(f"{status}: {description}")

# Test 4: Verify JavaScript functionality
print("\n" + "=" * 50)
print("TEST 4: JavaScript Functions")
print("=" * 50)

with open('app.js', 'r') as f:
    js_content = f.read()

required_functions = [
    ('addTask', 'add task function'),
    ('deleteTask', 'delete task function'),
    ('toggleTask', 'toggle task completion'),
    ('renderTasks', 'render tasks to DOM'),
    ('saveTasks', 'save tasks to localStorage'),
    ('updateStats', 'update task statistics')
]

for func_name, description in required_functions:
    has_func = f'function {func_name}' in js_content or f'{func_name} = ' in js_content
    status = "[PASS]" if has_func else "[FAIL]"
    print(f"{status}: {description}")

# Test 5: Verify key features
print("\n" + "=" * 50)
print("TEST 5: Key Features")
print("=" * 50)

features = [
    ('localStorage', 'persistence with localStorage'),
    ('Enter', 'add task on Enter key'),
    ('checkbox', 'mark task complete'),
    ('escapeHtml', 'XSS protection'),
    ('eventListener', 'event handlers attached')
]

for feature, description in features:
    has_feature = feature in js_content
    status = "[PASS]" if has_feature else "[FAIL]"
    print(f"{status}: {description}")

print("\n" + "=" * 50)
print("All tests completed!")
print("=" * 50)
