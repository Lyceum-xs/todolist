// script.js (V12 - 已修复筛选功能)

document.addEventListener('DOMContentLoaded', () => {

    // ===================================================================
    // 1. 全局配置与状态管理
    // ===================================================================
    const API_BASE_URL = 'http://127.0.0.1:8000';

    // --- 全局DOM元素获取 ---
    const navLinks = document.querySelectorAll('.nav-links li, .sidebar-footer a');
    const contentSections = document.querySelectorAll('.content-section');
    
    const taskListElement = document.querySelector('.task-list');
    const createTaskBtn = document.querySelector('.create-task-btn');
    const todayDateElement = document.getElementById('today-date');
    const filterButtons = document.querySelectorAll('.tasks-filter .filter-btn'); // 新增: 获取所有筛选按钮

    const habitGrid = document.querySelector('.habit-grid');
    const createHabitBtn = document.querySelector('.create-habit-btn');
    
    const calendarGrid = document.querySelector('.calendar-grid');
    const currentMonthYearElement = document.getElementById('current-month-year');
    const prevMonthBtn = document.getElementById('prev-month-btn');
    const nextMonthBtn = document.getElementById('next-month-btn');

    const pomodoroContainer = document.querySelector('.pomodoro-container');
    const pomodoroBtnMain = document.getElementById('pomodoro-btn-main');
    const pomodoroResetBtnMain = document.getElementById('pomodoro-reset-btn-main');
    const pomodoroSettingsBtnMain = document.getElementById('pomodoro-settings-btn-main');
    const timerDisplayMain = document.querySelector('.pomodoro-time-display');
    const pomodoroStatus = document.querySelector('.pomodoro-status');
    const progressCircle = document.querySelector('.circle-progress');

    // --- 全局状态变量 ---
    let calendarDate = new Date();
    let tasksCache = [];
    const circleRadius = 45;
    const circleCircumference = 2 * Math.PI * circleRadius;
    let mainTimerInterval;
    let mainTimerState = 'stopped'; // 'stopped', 'running', 'paused'
    let isWorkSession = true;
    let mainWorkMinutes = 25;
    let mainBreakMinutes = 5;
    let mainTimeInSeconds = mainWorkMinutes * 60;

    // ===================================================================
    // 2. 初始化
    // ===================================================================
    initializePage();

    function initializePage() {
        setupEventListeners();
        navigateTo('tasks-section');
        progressCircle.setAttribute('stroke-dasharray', circleCircumference);
        resetMainTimer();
        if(todayDateElement) {
             todayDateElement.textContent = `今天是 ${new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })}`;
        }
    }

    // ===================================================================
    // 3. 事件监听器设置
    // ===================================================================
    function setupEventListeners() {
        navLinks.forEach(link => { link.addEventListener('click', (e) => { e.preventDefault(); const targetId = link.getAttribute('data-target'); if (targetId) navigateTo(targetId); }); });
        if(createTaskBtn) createTaskBtn.addEventListener('click', () => openCreateTaskModal());
        if(taskListElement) taskListElement.addEventListener('click', handleTaskInteraction);
        
        // 新增: 为每个筛选按钮添加点击事件监听
        if(filterButtons) {
            filterButtons.forEach(btn => btn.addEventListener('click', handleFilterClick));
        }

        if(createHabitBtn) createHabitBtn.addEventListener('click', () => openCreateHabitModal());
        if(habitGrid) habitGrid.addEventListener('click', handleHabitInteraction);
        if(prevMonthBtn) prevMonthBtn.addEventListener('click', () => changeMonth(-1));
        if(nextMonthBtn) nextMonthBtn.addEventListener('click', () => changeMonth(1));
        if(pomodoroBtnMain) pomodoroBtnMain.addEventListener('click', handleMainTimerClick);
        if(pomodoroResetBtnMain) pomodoroResetBtnMain.addEventListener('click', () => resetMainTimer(false));
        if(pomodoroSettingsBtnMain) pomodoroSettingsBtnMain.addEventListener('click', () => openPomodoroSettingsModal());
    }
    
    // ===================================================================
    // 4. API 通信函数
    // ===================================================================
    async function fetchAPI(endpoint, options = {}) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            if (!response.ok) {
                let errorMessage = `HTTP 错误! 状态码: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || JSON.stringify(errorData);
                } catch (e) {
                    errorMessage = response.statusText || '无法连接到服务器';
                }
                throw new Error(errorMessage);
            }
            if (response.status === 204) return null;
            return await response.json();
        } catch (error) {
            console.error(`API调用失败 (${endpoint}):`, error);
            alert(`操作失败: ${error.message}`);
            throw error;
        }
    }
    
    // --- 任务API封装 ---
    async function fetchTasks() {
        tasksCache = await fetchAPI('/tasks');
        // 修改: 默认使用'all'过滤器渲染任务
        handleFilterClick(); 
        renderCalendar();
    }
    async function createTask(taskData) {
        await fetchAPI('/tasks', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(taskData) });
        await fetchTasks();
    }
    async function updateTask(taskId, taskData) {
        await fetchAPI(`/tasks/${taskId}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(taskData) });
    }
    async function deleteTask(taskId) {
        await fetchAPI(`/tasks/${taskId}`, { method: 'DELETE' });
        await fetchTasks();
    }

    // --- 习惯API封装 ---
    async function fetchHabits() {
        const habits = await fetchAPI('/habits');
        if (habits) renderHabits(habits);
    }
    async function createHabit(habitData) {
        await fetchAPI('/habits', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(habitData) });
        await fetchHabits();
    }
    async function deleteHabit(habitId) {
        await fetchAPI(`/habits/${habitId}`, { method: 'DELETE' });
        await fetchHabits();
    }
    async function checkInHabit(habitId, buttonElement) {
        await fetchAPI(`/habits/${habitId}/logs`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) });
        buttonElement.textContent = '今日已完成';
        buttonElement.classList.add('completed');
        await fetchHabitStreak(habitId);
    }
    async function fetchHabitStreak(habitId) {
        const streak = await fetchAPI(`/habits/${habitId}/streak`);
        const habitCard = document.querySelector(`.habit-card[data-habit-id="${habitId}"]`);
        if (habitCard) habitCard.querySelector('.habit-streak strong').textContent = streak;
    }

    // ===================================================================
    // 5. 渲染与交互处理
    // ===================================================================
    
    function navigateTo(targetId) {
        navLinks.forEach(item => { item.classList.toggle('active', item.getAttribute('data-target') === targetId); });
        contentSections.forEach(section => { section.classList.toggle('active', section.id === targetId); });
        if (targetId === 'tasks-section') fetchTasks();
        else if (targetId === 'habits-section') fetchHabits();
        else if (targetId === 'calendar-section') renderCalendar();
    }
    
    // 新增: 任务筛选处理函数
    function handleFilterClick(event) {
        let filter = 'all'; // 默认过滤器

        if (event) { // 如果是通过点击事件触发
            const clickedButton = event.currentTarget;
            filter = clickedButton.dataset.filter;
            filterButtons.forEach(btn => btn.classList.remove('active'));
            clickedButton.classList.add('active');
        } else { // 如果是初次加载或无事件触发
            // 保持'all'按钮的激活状态
             const allButton = document.querySelector('.filter-btn[data-filter="all"]');
             if(allButton) allButton.classList.add('active');
        }
        
        let filteredTasks = [];
        if (filter === 'all') {
            filteredTasks = tasksCache;
        } else if (filter === 'completed') {
            filteredTasks = tasksCache.filter(task => task.completed);
        } else if (filter === 'pending') {
            filteredTasks = tasksCache.filter(task => !task.completed);
        }
        
        renderTasks(filteredTasks);
    }

    function renderTasks(tasks) {
        taskListElement.innerHTML = '';
        if (!tasks || tasks.length === 0) { 
            taskListElement.innerHTML = '<li>太棒了，当前分类下没有任务！</li>'; 
            return; 
        }
        tasks.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).forEach(task => {
            const dueDateText = task.due_date ? new Date(task.due_date).toLocaleDateString() : '';
            const taskHTML = `
                <li class="task-item ${task.completed ? 'completed' : ''}" data-task-id="${task.id}">
                    <label class="checkbox-container"><input type="checkbox" ${task.completed ? 'checked' : ''}><span class="checkmark"></span></label>
                    <div class="task-details">
                        <p class="task-name">${task.name}</p>
                        <span class="task-due-date">${dueDateText}</span>
                    </div>
                    <div class="task-tags">${task.urgent ? '<span class="tag urgent">🔥</span>' : ''}${task.importance ? '<span class="tag important">⭐</span>' : ''}</div>
                    <button class="btn-delete" title="删除任务">🗑️</button>
                </li>`;
            taskListElement.insertAdjacentHTML('beforeend', taskHTML);
        });
    }

    function handleTaskInteraction(event) {
        const checkbox = event.target.closest('.checkbox-container input[type="checkbox"]');
        const deleteBtn = event.target.closest('.btn-delete');

        if (checkbox) {
            const taskItem = checkbox.closest('.task-item');
            const taskId = taskItem.dataset.taskId;
            const isCompleted = checkbox.checked;

            // 1. 立即在UI上反映变化，提供即时反馈
            taskItem.classList.toggle('completed', isCompleted);

            // 2. 在后台发送更新请求
            updateTask(taskId, { completed: isCompleted })
                .then(() => {
                    // 3. 更新成功后，在本地缓存中也更新这条记录
                    // 这一步很重要，确保了用户切换筛选时数据是正确的
                    const taskIndex = tasksCache.findIndex(t => t.id == taskId);
                    if (taskIndex > -1) {
                        tasksCache[taskIndex].completed = isCompleted;
                    }

                    // 4. 判断当前筛选状态，决定是否从视图中移除该项
                    const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;
                    
                    // 如果在“待办”页完成了一个任务，或在“已完成”页取消了一个任务，则将它移出视图
                    if ((activeFilter === 'pending' && isCompleted) || (activeFilter === 'completed' && !isCompleted)) {
                        // 添加一个简单的淡出动画，然后移除元素
                        taskItem.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
                        taskItem.style.opacity = '0';
                        taskItem.style.transform = 'translateX(20px)';
                        setTimeout(() => {
                            taskItem.remove();
                            // 检查列表是否为空，如果为空则显示提示信息
                            if (taskListElement.children.length === 0) {
                                taskListElement.innerHTML = '<li>太棒了，当前分类下没有任务！</li>';
                            }
                        }, 400);
                    }
                })
                .catch(() => {
                    // 5. 如果更新失败，撤销UI上的更改并提醒用户
                    alert('更新任务状态失败，已为您撤销操作！');
                    taskItem.classList.toggle('completed', !isCompleted);
                    checkbox.checked = !isCompleted;
                });
            return;
        }

        if (deleteBtn) {
            const taskItem = deleteBtn.closest('.task-item');
            const taskId = taskItem.dataset.taskId;
            openConfirmModal('您确定要删除这个任务吗？', () => {
                deleteTask(taskId).catch(() => {});
            });
        }
    }

    function renderHabits(habits) {
        habitGrid.innerHTML = '';
        if (!habits || habits.length === 0) { habitGrid.innerHTML = '<p>还没有养成任何习惯，快来创建一个吧！</p>'; return; }
        habits.forEach(habit => {
            const todayStr = new Date().toISOString().split('T')[0];
            const hasCheckedInToday = habit.logs.some(log => log.date.startsWith(todayStr));
            const habitHTML = `
                <div class="habit-card" data-habit-id="${habit.id}">
                    <button class="btn-delete btn-delete-habit" title="删除习惯">🗑️</button>
                    <div class="habit-icon">📝</div>
                    <div class="habit-info">
                        <h3>${habit.name}</h3>
                        <p>${habit.description || ''}</p>
                    </div>
                    <div class="habit-streak">🔥 已坚持 <strong>...</strong> 天</div>
                    <button class="btn btn-check-in ${hasCheckedInToday ? 'completed' : ''}">${hasCheckedInToday ? '今日已完成' : '今日打卡'}</button>
                </div>`;
            habitGrid.insertAdjacentHTML('beforeend', habitHTML);
            fetchHabitStreak(habit.id);
        });
    }

    function handleHabitInteraction(event) {
        const checkInBtn = event.target.closest('.btn-check-in');
        const deleteBtn = event.target.closest('.btn-delete-habit');

        if (checkInBtn && !checkInBtn.classList.contains('completed')) {
            const habitId = checkInBtn.closest('.habit-card').dataset.habitId;
            checkInHabit(habitId, checkInBtn).catch(() => {});
            return;
        }

        if (deleteBtn) {
            const habitId = deleteBtn.closest('.habit-card').dataset.habitId;
            openConfirmModal('您确定要删除这个习惯吗？', () => {
                deleteHabit(habitId).catch(() => {});
            });
        }
    }

    function renderCalendar() {
        calendarGrid.innerHTML = '<div class="day-name">日</div><div class="day-name">一</div><div class="day-name">二</div><div class="day-name">三</div><div class="day-name">四</div><div class="day-name">五</div><div class="day-name">六</div>';
        const year = calendarDate.getFullYear();
        const month = calendarDate.getMonth();
        currentMonthYearElement.textContent = `${year}年 ${month + 1}月`;
        
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        for (let i = 0; i < firstDayOfMonth; i++) {
            calendarGrid.insertAdjacentHTML('beforeend', '<div class="day-cell other-month"></div>');
        }
        for (let i = 1; i <= daysInMonth; i++) {
            const dayCell = document.createElement('div');
            dayCell.classList.add('day-cell');
            dayCell.innerHTML = `<div class="day-number">${i}</div>`;
            const today = new Date();
            if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayCell.querySelector('.day-number').classList.add('today');
            }
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            const tasksForDay = (tasksCache || []).filter(task => task.due_date && task.due_date.startsWith(dateStr));
            if (tasksForDay.length > 0) {
                const tasksContainer = document.createElement('div');
                tasksContainer.className = 'calendar-tasks';
                tasksForDay.slice(0, 3).forEach(task => { const taskEl = document.createElement('div'); taskEl.className = 'calendar-task-item'; taskEl.textContent = task.name; tasksContainer.appendChild(taskEl); });
                dayCell.appendChild(tasksContainer);
            }
            calendarGrid.appendChild(dayCell);
        }
    }
    function changeMonth(offset) {
        calendarDate.setMonth(calendarDate.getMonth() + offset);
        renderCalendar();
    }
    
    // ===================================================================
    // 6. 组件逻辑 (番茄钟, 弹窗)
    // ===================================================================
    
    function updateCircleProgress(percent) {
        const offset = circleCircumference * (1 - percent);
        progressCircle.style.strokeDashoffset = offset;
    }
    function updateMainTimerDisplay() {
        const minutes = Math.floor(mainTimeInSeconds / 60);
        const seconds = mainTimeInSeconds % 60;
        timerDisplayMain.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
    function resetMainTimer(switchToNext = false) {
        clearInterval(mainTimerInterval);
        if (switchToNext) isWorkSession = !isWorkSession;
        pomodoroContainer.className = 'pomodoro-container';
        if (isWorkSession) {
            mainTimeInSeconds = mainWorkMinutes * 60;
            pomodoroStatus.textContent = '专注时间';
            pomodoroContainer.classList.add('work-mode');
        } else {
            mainTimeInSeconds = mainBreakMinutes * 60;
            pomodoroStatus.textContent = '休息一下';
            pomodoroContainer.classList.add('break-mode');
        }
        mainTimerState = 'stopped';
        pomodoroBtnMain.textContent = '▶️ 开始';
        updateMainTimerDisplay();
        updateCircleProgress(1);
    }
    function handleMainTimerClick() {
        if (mainTimerState === 'stopped' || mainTimerState === 'paused') {
            mainTimerState = 'running';
            pomodoroBtnMain.textContent = '⏸️ 暂停';
            const totalDuration = mainTimeInSeconds > 0 ? mainTimeInSeconds : (isWorkSession ? mainWorkMinutes : mainBreakMinutes) * 60;
            mainTimerInterval = setInterval(() => {
                mainTimeInSeconds--;
                updateCircleProgress(mainTimeInSeconds / totalDuration);
                updateMainTimerDisplay();
                if (mainTimeInSeconds < 0) {
                    alert(isWorkSession ? '专注结束！' : '休息结束！');
                    resetMainTimer(true);
                }
            }, 1000);
        } else if (mainTimerState === 'running') {
            mainTimerState = 'paused';
            clearInterval(mainTimerInterval);
            pomodoroBtnMain.textContent = '▶️ 继续';
        }
    }
    
    function createModal(title, bodyHTML, footerHTML, onSave) {
        const modalId = `modal-${Date.now()}`;
        const modalHTML = `<div class="modal-overlay" id="${modalId}"><div class="modal-content"><div class="modal-header"><h2>${title}</h2><button class="modal-close-btn">&times;</button></div><div class="modal-body">${bodyHTML}</div><div class="modal-footer">${footerHTML}</div></div></div>`;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const overlay = document.getElementById(modalId);
        const closeModal = () => overlay.remove();
        overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
        overlay.querySelector('.modal-close-btn').addEventListener('click', closeModal);
        
        const secondaryBtn = overlay.querySelector('.btn-secondary');
        if (secondaryBtn) secondaryBtn.addEventListener('click', closeModal);
        
        const primaryBtn = overlay.querySelector('.btn-primary');
        if (primaryBtn && onSave) {
            primaryBtn.addEventListener('click', () => { onSave(overlay); });
        }
        return overlay;
    }

    function openConfirmModal(message, onConfirm) {
        const body = `<p style="margin: 0; padding: 16px 0; font-size: 16px;">${message}</p>`;
        const footer = `<button class="btn btn-secondary">取消</button><button class="btn btn-danger">确定删除</button>`;
        const modal = createModal('请确认', body, footer, null);

        modal.querySelector('.btn-danger').addEventListener('click', () => {
            onConfirm();
            modal.remove();
        });
    }

    function openCreateTaskModal() {
        const body = `<div class="form-group"><label for="task-name-input">任务名称</label><input type="text" id="task-name-input" placeholder="例如：学习 JavaScript"></div><div class="form-group"><label for="task-desc-input">描述</label><textarea id="task-desc-input" rows="3" placeholder="添加更详细的说明..."></textarea></div><div class="form-group"><label for="task-due-date-input">截止日期</label><input type="text" id="task-due-date-input" placeholder="选择日期..."></div><div class="form-group-inline"><label><input type="checkbox" id="task-important-input"> 重要</label><label><input type="checkbox" id="task-urgent-input"> 紧急</label></div>`;
        const footer = `<button class="btn btn-secondary">取消</button><button class="btn btn-primary">保存任务</button>`;

        const modal = createModal('创建新任务', body, footer, (m) => {
            const saveBtn = m.querySelector('.btn-primary');
            const originalBtnText = saveBtn.textContent;
            const taskData = {
                name: m.querySelector('#task-name-input').value,
                description: m.querySelector('#task-desc-input').value,
                due_date: m.querySelector('#task-due-date-input').value || null,
                importance: m.querySelector('#task-important-input').checked,
                urgent: m.querySelector('#task-urgent-input').checked
            };
            if (!taskData.name) { alert('任务名称不能为空！'); return; }
            saveBtn.disabled = true;
            saveBtn.textContent = '保存中...';
            createTask(taskData).then(() => { m.remove(); }).catch(() => { saveBtn.disabled = false; saveBtn.textContent = originalBtnText; });
        });
        flatpickr(modal.querySelector("#task-due-date-input"), { locale: "zh", dateFormat: "Y-m-d" });
    }
    
    function openCreateHabitModal() {
        const body = `<div class="form-group"><label for="habit-name-input">习惯名称</label><input type="text" id="habit-name-input" placeholder="例如：每日阅读"></div><div class="form-group"><label for="habit-desc-input">描述</label><textarea id="habit-desc-input" rows="3" placeholder="添加鼓励自己的话..."></textarea></div>`;
        const footer = `<button class="btn btn-secondary">取消</button><button class="btn btn-primary">保存习惯</button>`;

        createModal('创建新习惯', body, footer, (m) => {
            const saveBtn = m.querySelector('.btn-primary');
            const originalBtnText = saveBtn.textContent;
            const habitData = { name: m.querySelector('#habit-name-input').value, description: m.querySelector('#habit-desc-input').value };
            if (!habitData.name) { alert('习惯名称不能为空！'); return; }
            saveBtn.disabled = true;
            saveBtn.textContent = '保存中...';
            createHabit(habitData).then(() => { m.remove(); }).catch(() => { saveBtn.disabled = false; saveBtn.textContent = originalBtnText; });
        });
    }

    function openPomodoroSettingsModal() {
        const body = `<div class="form-group"><label for="work-minutes-input">专注时长（分钟）</label><input type="number" id="work-minutes-input" value="${mainWorkMinutes}"></div><div class="form-group"><label for="break-minutes-input">休息时长（分钟）</label><input type="number" id="break-minutes-input" value="${mainBreakMinutes}"></div>`;
        const footer = `<button class="btn btn-secondary">取消</button><button class="btn btn-primary">保存</button>`;
        createModal('番茄钟设置', body, footer, (m) => {
            mainWorkMinutes = parseInt(m.querySelector('#work-minutes-input').value) || 25;
            mainBreakMinutes = parseInt(m.querySelector('#break-minutes-input').value) || 5;
            resetMainTimer(false);
            m.remove();
        });
    }
});