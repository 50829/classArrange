// 定义数据类型
interface WeekInfo {
    start_week: number;
    end_week: number;
    week_type: string | null;
}

interface TimeSlot {
    day_of_week: number;
    periods: number[];
}

interface ParsedTimeLocation {
    week_info: WeekInfo;
    campus: number;
    time_slots: TimeSlot[];
}

interface ClassNumberGroup {
    class_number_group_id: number;
    course_number: string;
    class_numbers: string[];
    course_name: string;
    credit: number;
    assessment_method: string;
    parsed_time_location: ParsedTimeLocation[];
}

// 声明全局变量
declare const infoCreateTime: string;
declare const classInfo: any[];
declare const groupInfo: ClassNumberGroup[];

// 应用类
class CourseGroupApp {
    private selectedGroupsContainer: HTMLElement;
    private selectedGroupIds: Set<number>;

    constructor() {
        // 初始化DOM元素
        this.selectedGroupsContainer = document.getElementById('selected-groups-container')!;
        
        // 初始化已选课程组ID集合
        this.selectedGroupIds = this.loadSelectedGroupsFromStorage();

        // 初始化应用
        this.init();
    }

    private init(): void {
        // 初始化应用
        this.updateSelectedGroupsDisplay();
    }

    // 从localStorage加载已选课程组
    private loadSelectedGroupsFromStorage(): Set<number> {
        const stored = localStorage.getItem('selectedCourseGroups');
        if (stored) {
            try {
                return new Set(JSON.parse(stored).map(Number));
            } catch (e) {
                console.error('Failed to parse selected groups from localStorage:', e);
                return new Set();
            }
        }
        return new Set();
    }

    // 将已选课程组保存到localStorage
    private saveSelectedGroupsToStorage(): void {
        localStorage.setItem('selectedCourseGroups', JSON.stringify(Array.from(this.selectedGroupIds)));
    }

    // 处理删除课程组
    private handleRemoveGroup(groupId: number): void {
        this.selectedGroupIds.delete(groupId);
        
        // 保存到localStorage
        this.saveSelectedGroupsToStorage();
        
        // 更新已选课程组显示
        this.updateSelectedGroupsDisplay();
    }

    // 更新已选课程组显示
    private updateSelectedGroupsDisplay(): void {
        if (this.selectedGroupIds.size === 0) {
            this.selectedGroupsContainer.innerHTML = '<p class="no-selections">暂无选择的课程组</p>';
            return;
        }

        // 获取已选课程组的详细信息
        const selectedGroups = Array.from(this.selectedGroupIds)
            .map(id => groupInfo.find(group => group.class_number_group_id === id))
            .filter((group): group is ClassNumberGroup => group !== undefined);

        // 渲染已选课程组
        this.selectedGroupsContainer.innerHTML = selectedGroups.map(group => `
            <div class="selected-group-item" data-group-id="${group.class_number_group_id}">
                <span class="group-info">
                    ${group.course_name} (ID: ${group.class_number_group_id})<br>
                    <small>课程编号: ${group.course_number} | 课堂编号: ${this.formatClassNumbers(group.class_numbers)}</small>
                </span>
                <button class="remove-btn" data-group-id="${group.class_number_group_id}">
                    ×
                </button>
            </div>
        `).join('');

        // 绑定删除按钮事件
        this.selectedGroupsContainer.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const groupId = parseInt((e.target as HTMLElement).dataset.groupId!);
                this.handleRemoveGroup(groupId);
            });
        });
    }

    // 格式化课堂编号
    private formatClassNumbers(classNumbers: string[]): string {
        if (classNumbers.length > 10) {
            return '很多';
        }
        return classNumbers.join(',');
    }
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new CourseGroupApp();
});