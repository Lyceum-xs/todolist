# CI/CD 技术文档

* **文档版本：** V1.0
* **编写人：** 李锡浩 杨晓舒
* **编写日期：** 2025年07月05日
---

**目录**
- [CI/CD 技术文档](#cicd-技术文档)
    - [1.简介](#1简介)
      - [1.1 目的](#11-目的)
      - [1.2 范围](#12-范围)
    - [2. CI/CD 流水线概述](#2-cicd-流水线概述)
    - [3. Jenkins 自动化构建](#3-jenkins-自动化构建)
      - [3.1 Jenkins Job 配置](#31-jenkins-job-配置)
        - [3.1.1 源码管理 (SCM)](#311-源码管理-scm)
        - [3.1.2 构建步骤](#312-构建步骤)
    - [4. Ansible 自动化部署](#4-ansible-自动化部署)
      - [4.1. Ansible Playbook](#41-ansible-playbook)
      - [4.2.Playbook 结构与功能](#42playbook-结构与功能)
        - [4.2.1 变量](#421-变量)
        - [4.2.2 部署任务](#422-部署任务)
      - [4.3 Ansible 与 Jenkins 的集成](#43-ansible-与-jenkins-的集成)
    - [5.SonarQube 代码质量检测](#5sonarqube-代码质量检测)
    - [6. 监控与日志](#6-监控与日志)


### 1.简介
本文档旨在详细阐述 [to do list] 的持续集成/持续部署（CI/CD）流水线。该流水线实现了从代码提交到部署的自动化软件交付流程
#### 1.1 目的
此CI/CD 流水线的主要目的是：
- 自动化构建和测试过程。
- 自动化应用程序到不同环境的部署。
- 减少人工错误，提高效率。

#### 1.2 范围
本文档涵盖了Jenkins自动化构建和Ansible自动化部署在CI/CD工作流中的集成和配置。  

---

### 2. CI/CD 流水线概述
CI/CD 流水线被设计为一系列自动化步骤，当代码发生变化时触发。其大致流程如下：

1. **代码提交：** 开发人员将代码提交到 Git 仓库。

2. **Jenkins 构建触发：** Jenkins 自动检测代码更改并触发新的构建。

3. **自动化构建与测试：** Jenkins 编译代码，运行单元测试，并打包应用程序。

4. **构件生成：** 生成一个可部署的构件

5. **Ansible 部署触发：** 构建成功后，Jenkins 触发 Ansible 进行部署。

---

### 3. Jenkins 自动化构建
Jenkins 作为核心自动化服务器，负责编排CI/CD流水线中的构建和初步测试阶段。
#### 3.1 Jenkins Job 配置
每个项目通常都有一个专用的 Jenkins Job（或流水线中的一系列 Job），用于执行构建过程。

##### 3.1.1 源码管理 (SCM)
Jenkins 配置从 GitLab 拉取代码。SCM 被设置每30分钟检测 GitLab上是否有提交  

**Jenkins SCM配置图**
![alt text](./assets/SCM.png)


##### 3.1.2 构建步骤
构建步骤包括编译源代码、解析依赖项以及运行自动化测试。
- 测试框架： 集成了 Pytest 以确保代码质量。

**Jenkins构建脚本**
```bash
cd /var/lib/jenkins/workspace/to_do_list

echo "创建并激活 Jenkins 测试环境的虚拟环境..."
python3 -m venv venv_test
. venv_test/bin/activate

echo "安装项目和测试依赖..."
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install -r requirements-dev.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "运行 Pytest 测试 (位于 tests/unit)..."
pytest --junitxml=test-results.xml tests/unit/

if [ $? -ne 0 ]; then
    echo "Pytest tests failed! Aborting deployment."
    exit 1 # 强制 Jenkins 构建失败
fi

echo "测试通过，执行 Ansible 部署..."
ansible-playbook deploy_todolist.yml -c local
```

![alt text](./assets/jenkins1.png)

---

### 4. Ansible 自动化部署
#### 4.1. Ansible Playbook
Ansible Playbook 是用于执行部署任务的核心文件，以 YAML 格式编写，描述了要执行的操作序列。
```yaml
- name: 部署任务管理系统
  hosts: localhost # 目标主机

  vars:
    repo_url: http://whucsgitlab.whu.edu.cn/devops/todolist.git
    base_install_dir: /opt
    app_base_dir: "{{ base_install_dir }}/todolist"
    app_full_path: "{{ app_base_dir }}/src/app"
    app_log_file: "{{ app_full_path }}/app.log"
    venv_path: "{{ app_full_path }}/venv"
    production_requirements_file: "{{ app_base_dir }}/requirements.txt"
    main_app_file: "main"
    jenkins_user: jenkins
    jenkins_group: jenkins
  tasks:
    - name: 确保基础安装目录存在
      ansible.builtin.file:
        path: "{{ base_install_dir }}"
        state: directory
        mode: '0755'
        owner: root
        group: root
      when: base_install_dir != '/tmp'
      become: yes

    - name: 确保项目根目录存在且所有者是Jenkins用户 (root 权限创建并更改所有权)
      ansible.builtin.file:
        path: "{{ app_base_dir }}" # /opt/todolist
        state: directory
        mode: '0755'
        owner: "{{ jenkins_user }}"
        group: "{{ jenkins_group }}"
        recurse: yes
      become: yes

    - name: 创建Python虚拟环境
      ansible.builtin.command:
        cmd: python3 -m venv "{{ venv_path }}"
        chdir: "{{ app_full_path }}"
      args:
        creates: "{{ venv_path }}/bin/activate"

    - name: 安装Python依赖
      ansible.builtin.pip:
        requirements: "{{ production_requirements_file }}"
        virtualenv: "{{ venv_path }}"
        extra_args: "-i https://pypi.tuna.tsinghua.edu.cn/simple"

    - name: 停止旧的应用进程 (如果存在)
      ansible.builtin.shell: |
        ps aux | grep "{{ main_app_file }}" | grep -v grep | awk '{print $2}' | xargs -r kill -9
      changed_when: true

    - name: 后台启动应用
      ansible.builtin.shell: |
        nohup {{ venv_path }}/bin/python -m src.app.main > "{{ app_log_file }}" 2>&1 &
      args:
        chdir: "{{ app_base_dir }}" # 在主应用程序文件所在的目录执行启动命令
      async: 1 # 异步执行，不等待命令完成
      poll: 0  # 不轮询结果，立即返回
```
#### 4.2.Playbook 结构与功能

##### 4.2.1 变量

Playbook 预定义了部署相关的关键信息：

- `repo_url`: 项目代码的 Git 仓库地址。

- `base_install_dir`: 应用程序的基础安装目录（默认为 /opt）。

- `app_base_dir`: 应用程序项目根目录（/opt/todolist）。

- `app_full_path`: 应用程序主代码路径（{{ app_base_dir }}/src/app）。

- `app_log_file`: 应用程序日志文件路径。

- `venv_path`: Python 虚拟环境路径。

- `production_requirements_file`: 生产环境 Python 依赖文件路径。

- `main_app_file`: 应用程序主入口文件名（main）。

- `jenkins_user`, `jenkins_group`: Jenkins 用户和组，用于设置目录所有权。

##### 4.2.2 部署任务
以下是 Playbook 自动执行的部署任务序列：

1. **环境准备**：
- 确保基础安装目录 (`/opt`) 存在并设置 `root` 权限。
- 创建或确认项目根目录 (`/opt/todolist`) 存在，并设置其所有者为 Jenkins 用户，以便 Jenkins 有权限管理.

2. **依赖管理**：
- 在应用程序主目录 (src/app) 内创建 Python 虚拟环境。
- 在虚拟环境中，根据 `requirements.txt` 安装所有生产环境依赖，并使用清华 PyPI 镜像加速下载。

3. **应用管理**：
- 停止所有可能存在的旧应用进程，避免端口冲突。
- 以后台模式启动应用程序，将输出重定向到日志文件 (`app.log`)。此步骤为异步执行，不阻塞后续流程。

#### 4.3 Ansible 与 Jenkins 的集成
Jenkins 通过执行 `ansible-playbook deploy_todolist.yml -c local` 命令来触发此部署 Playbook。此命令指示 Ansible 在本地执行部署任务，与 Playbook 中 hosts: localhost 的定义一致。

---

### 5.SonarQube 代码质量检测
有一些警告（如：维护性问题、测试覆盖率低、安全热点），但质量门总体通过，说明没有阻碍代码发布的重大问题。  
各项指标分析（以最后一张图为准）
1. **Security（安全）**
  - Open issues: 0（等级 A）
  - 没有已识别的安全漏洞，表现很好。 3（等级 E）
2. **Security Hotspots:**
  -	存在 3 个“安全热点”，是潜在的安全问题（如使用敏感 API、用户输入未校验等）。
  -	等级为 E（严重），这并不意味着存在实际漏洞，而是 SonarQube 出于“安全审慎”立场，对一些敏感操作或关键逻辑进行了提示性标记。
3. **Reliability（可靠性）**
  -	5 个 open issues（等级 A）
  -	一些小的错误或潜在问题（如异常未处理、null 可能引用等），问题数量不多，评级为 A，表现良好。
4. **Maintainability（可维护性）**
  -	54 个 open issues（等级 C）
  -	问题数量偏多，常见如重复代码、代码风格不一致、函数过长、变量命名不清晰等。
  -	等级为 C，说明代码在可读性和维护上还有较大改进空间。
5. **Coverage（测试覆盖率）**
  -	15.8% 的覆盖率（等级低）
  - 共有 1700 行代码需覆盖，仅覆盖 15.8%。
6. **Duplications（代码重复）**
  -	0.0%（等级 A）
  - 没有检测到重复代码，结构性很好。
![alt text](./assets/sonarCI1.png)
![alt text](./assets/sonarCI2.png)
通过测试单元的修改，覆盖率增加
![alt text](./assets/sonarCI3.png)

### 6. 监控与日志

为了确保 CI/CD 流水线的健康运行，需要对 Jenkins 构建日志和 Ansible 部署日志进行有效监控。

- **Jenkins 日志：** 每次构建都会生成详细日志，记录了构建过程中的每一步骤和任何错误信息。

- **Ansible 日志：** Ansible 每次执行 Playbook 也会生成日志，记录了部署任务的执行结果和遇到的问题。

![alt text](./assets/log.png)