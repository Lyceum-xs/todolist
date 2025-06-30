### 项目周报模板

**使用说明：**
*   本周报旨在帮助你总结每周的工作进展、遇到的问题、学习收获以及规划下周任务。
*   请务必如实填写，这不仅是对项目进度的跟踪，也是你自我反思和成长的过程。
*   对于学生项目，尤其要注重“心得体会与学习收获”部分，这能体现你的学习能力和解决问题的能力。
*   建议每周固定时间填写并提交（如果项目有导师或团队）。

---

#### **[ToDoList] 周报**

**报告周期：** 2025年年06月22日 至 2025年06月30日
**报告人：** 杨晓舒
**报告日期：** 2025年06月30日

---

**一、 基本信息**

*   **项目名称：** ToDoList
*   **当前项目阶段：** 模块开发 & 单元测试阶段
*   **本周总工时：** 40小时

---

**二、 本周完成工作**

*   **目标达成情况：**
    *   上周设定的“打通核心数据模型 + 完成服务层单元测试”目标已 100 % 达成
*   **具体完成任务列表：**
    *   数据模型重构：[重新设计 Task 的 父子任务关系（parent / subtasks），明确 uselist=False，解决级联删除异常]
    *   Habit 模块完善：[为 HabitLog 增加 (habit_id, date) 唯一约束，避免重复打卡]
    *   测试环境搭建：[编写 conftest.py：内存 SQLite + monkeypatch 新增 test_models.py & test_services.py；全部 4 条用例通过]
    *   CI 预配置：[初步编写 .gitlab-ci.yml 测试阶段脚本（pytest + coverage）]
    *   Bug 修复：[解决 src/api/__init__.py 编码导致 pytest 收集失败的问题 处理 Pydantic / SQLAlchemy 2.x 警告，临时通过 pytest.ini muted]

---

**三、 未完成工作及原因**

*   **未完成任务列表：**
    *   API 层集成测试（test_api.py）
    *   **原因：** [编码修复后尚未补充有效断言，需要等待接口稳定]

---

**四、 遇到的问题与困难**

*   **技术问题：**
    *   SQLAlchemy LegacyAPIWarning 大量输出
    *   **已尝试的解决方案：** [按官方建议将 query.get() 替换为 session.get()；大部分已修改]
    *   **需要帮助或待解决：** [剩余少量调用点待搜索替换]
*   **非技术问题：**
    *   前端后端太过分离
    *   **已采取的措施：** [先做成一体，后续再进行分离]

---

**五、 下周计划**

*   **主要目标：**
    *   1.	完成 REST API 集成测试 并接入 GitLab CI
	    2.	修正警告，至少清零 SQLAlchemy LegacyAPIWarning
*   **具体任务列表：**
    *   编写 tests/api/test_task_endpoints.py：[新增 ≥ 6 条接口用例全部通过（预计一天）]
    *   Habit 打卡接口 PUT/PATCH 支持：[Swagger 文档同步更新(预计半天)]
    *  升级 Pydantic 配置写法：[消除相关 DeprecationWarning]

---

**六、 心得体会与学习收获**

*   **本周学习到的新知识/技能：**
    *   [理解了 SQLAlchemy 2.x 新 API 与旧查询方式差异
    *   掌握 pytest fixture + monkeypatch 构造隔离数据库的技巧]
*   **对项目或开发流程的思考：**
    *   [深刻体会到 先写测试再refactor 的价值，避免了多处隐形 bug]
*   **自我改进方面：**
    *   [时间预估仍有偏差，下周将更细分任务颗粒度]

---

**七、 附件 (可选)**

*   [见gitlab仓库
*   https://whucsgitlab.whu.edu.cn/devops/todolist
*   ]

---

