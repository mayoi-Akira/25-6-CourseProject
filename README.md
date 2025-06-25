# 机器学习数据及模型托管平台

本项目为课程设计任务

包含前端（Vue3 + Element Plus）和后端（Flask + MySQL）两部分

- done:
   - 用户注册登录
   - 主页

- doing:
  - 数据集管理

- todo:
  - 模型训练
  - 使用模型预测

## 目录结构

```
├── flask/                # 后端 Flask 服务
│   ├── app.py            # Flask 启动入口
│   ├── sql_connect.py    # 数据库连接
│   └── user/             # 各功能模块
│       ├── login.py      # 登录注册接口
│       ├── dataset.py    # 数据集管理接口
│       ├── get_data.py   # 统计、用户信息、视频接口
│       └── ...
├── vue/                  # 前端 Vue3
│   ├── src/
│   │   ├── views/        # 页面视图
│   │   ├── components/   # 组件
│   │   └── ...
│   ├── public/
│   └── ...
└── README.md             # 项目说明
```

## 预计主要功能

- 用户注册、登录、登出
- 数据集上传、展示、删除、分页、搜索
- 模型管理与实验评测
- 统计信息展示
- 支持 zip 格式数据集上传与自动解压
- 权限与角色管理

## 前端启动

1. 进入 `vue` 目录
2. 安装依赖：
   ```bash
   npm install vue@3 vue-router@4 element-plus @element-plus/icons-vue typescript
   ```
   ```bash
   npm install vite --save-dev
   ```
3. 启动开发服务器：
   ```bash
   npm run dev
   ```
4. 访问 https://localhost:5173

## 后端启动

1. 进入 `flask` 目录
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 启动 Flask 服务：
   ```bash
   python app.py
   ```
4. 默认监听 5000 端口

## 数据库说明

- 使用 MySQL，需提前建库建表，表结构见 [SQL文件](./MySQL/root.sql)。
- 主要表：users、datasets、models、experiments、now

## 注意事项

- 前后端接口通过 CORS 跨域
- 上传仅支持 zip 文件，自动解压到指定目录，预计检测压缩包中必须包含对应数据集的 dataloader