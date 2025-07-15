#!/bin/bash

# 目标目录
INPUT_DIR="./"
# 输出文件名
OUTPUT_FILE="雅思part1合集_1.pdf"

# 创建一个临时目录，保存带章节标题的临时文件
TEMP_DIR=$(mktemp -d)

# 遍历目录下所有 .md 文件，并为每个文件生成一个包含标题的临时文件
for file in "$INPUT_DIR"/*.md; do
    # 提取文件名，不包括路径和扩展名
    FILENAME=$(basename "$file" .md)
    
    # 在临时文件中，先写入文件名作为一级标题（章节名）
    echo "# $FILENAME" > "$TEMP_DIR/$FILENAME.md"
    
    # 追加原始 Markdown 文件的内容到临时文件
    cat "$file" >> "$TEMP_DIR/$FILENAME.md"
done

# 获取所有临时文件
FILES=$(find "$TEMP_DIR" -type f -name "*.md" | sort | while read -r file; do echo "\"$file\""; done)

# 使用 pandoc 将所有临时文件转换为 PDF，每个文件名作为章节标题
eval pandoc $FILES -o "$OUTPUT_FILE" --pdf-engine=xelatex --toc

# 删除临时目录
rm -r "$TEMP_DIR"

echo "PDF 已生成: $OUTPUT_FILE"
