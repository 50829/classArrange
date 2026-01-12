import json

# 检查classNumberGroup.json
print("=== Checking classNumberGroup.json ===")
with open('classNumberGroup.json', 'r', encoding='utf-8') as f:
    groups = json.load(f)

# 检查第一个group
first_group = groups[0]
group_id = first_group['class_number_group_id']
print(f"First group_id: {group_id}")
print(f"Type: {type(group_id).__name__}")
print(f"Has 'group_' prefix: {str(group_id).startswith('group_')}")

# 检查classInfo_processed_with_group_id.json
print("\n=== Checking classInfo_processed_with_group_id.json ===")
with open('classInfo_processed_with_group_id.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

# 检查第一个课程
first_course = courses[0]
course_group_id = first_course['class_number_group_id']
print(f"First course group_id: {course_group_id}")
print(f"Type: {type(course_group_id).__name__}")

# 检查是否有null值
null_count = sum(1 for c in courses if c['class_number_group_id'] is None)
print(f"\nNumber of courses with null group_id: {null_count}")

# 检查课程号是否一致
print("\n=== Checking course_number consistency ===")
group_to_course_numbers = {}
for course in courses:
    group_id = course['class_number_group_id']
    course_number = course['course_number']
    if group_id not in group_to_course_numbers:
        group_to_course_numbers[group_id] = set()
    group_to_course_numbers[group_id].add(course_number)

# 检查是否有group包含多个course_number
error_count = sum(1 for g, cn in group_to_course_numbers.items() if len(cn) > 1)
print(f"Groups with multiple course_numbers: {error_count}")

# 总结
print("\n=== Summary ===")
if (not str(group_id).startswith('group_') and 
    type(group_id).__name__ == 'int' and 
    null_count == 0 and 
    error_count == 0):
    print("✓ Success: All conditions met!")
else:
    print("✗ Failure: Some conditions not met!")
