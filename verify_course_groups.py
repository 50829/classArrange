import json

# 读取处理后的课程数据
with open('classInfo_processed_with_group_id.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

# 创建一个映射：group_id -> [list of course_numbers]
group_to_course_numbers = {}

for course in courses:
    group_id = course['class_number_group_id']
    course_number = course['course_number']
    
    if group_id not in group_to_course_numbers:
        group_to_course_numbers[group_id] = []
    group_to_course_numbers[group_id].append(course_number)

# 检查每个group是否只包含一个course_number
error_groups = 0
for group_id, course_numbers in group_to_course_numbers.items():
    unique_course_numbers = set(course_numbers)
    if len(unique_course_numbers) > 1:
        print(f"Error: Group {group_id} contains multiple course_numbers: {unique_course_numbers}")
        error_groups += 1

# 输出结果
print(f"\nVerification complete:")
print(f"Total groups: {len(group_to_course_numbers)}")
print(f"Groups with multiple course_numbers: {error_groups}")

if error_groups == 0:
    print("✓ Success: All groups contain only one course_number")
else:
    print("✗ Failure: Some groups contain multiple course_numbers")
