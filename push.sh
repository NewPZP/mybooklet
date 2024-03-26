#!/bin/bash

# 设置 GitHub 仓库的相关信息
BRANCH_NAME="main"


# 添加所有更改的文件
git add .

# 提交更改
read -p "输入提交信息: " commit_message
git commit -m "$commit_message"

# 推送代码到 GitHub
git push origin $BRANCH_NAME

echo "代码已成功推送到 GitHub。"
