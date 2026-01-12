import json

# 读取classNumberGroup.json文件
with open('classNumberGroup.json', 'r', encoding='utf-8') as f:
    groups = json.load(f)

# 读取classInfo_processed_with_group_id.json文件
with open('classInfo_processed_with_group_id.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

# 验证每个group
valid_groups = 0
error_groups = 0

for group in groups:
    group_id = group['class_number_group_id']
    group_course_number = group['course_number']
    class_numbers = group['class_numbers']
    
    print(f"Checking group {group_id} (course_number: {group_course_number}) with class_numbers: {class_numbers}")
    
    # 对于group中的每个class_number，查找对应的课程并检查course_number是否一致
    is_valid = True
    for class_num in class_numbers:
        # 查找对应的课程
        matching_courses = [course for course in courses 
                          if course['class_number'] == class_num 
                          and course['course_number'] == group_course_number]
        
        if not matching_courses:
            # 找不到对应的课程，或者课程的course_number不匹配
            print(f"  Error: class_number {class_num} not found with course_number {group_course_number}")
            is_valid = False
    
    if is_valid:
        valid_groups += 1
        print("  ✓ Group is valid")
    else:
        error_groups += 1

print(f"\nVerification complete:")
print(f"Total groups: {len(groups)}")
print(f"Valid groups: {valid_groups}")
print(f"Error groups: {error_groups}")

if error_groups == 0:
    print("All groups are valid - each group contains only one course_number")
else:
    print("Some groups contain different course_numbers!")
