# Copyright Forge Skill — Codex reliability edition

以 [Rodert/copyright-forge-skill](https://github.com/Rodert/copyright-forge-skill) 为基础的软著材料生成 Skill 增强版。原作者及贡献者享有其原有权利；本仓库保留原始 [Apache-2.0 许可证](LICENSE)。**本项目为独立修改版，并非上游作者发布的官方版本。**

## 主要能力

面向 Codex、Claude Code 等支持 Agent Skills 的工具，将真实源代码仓库转化为软件著作权登记准备材料：功能证据、事实确认、源程序鉴别材料、软件说明书以及质量核查报告。

本版相较于上游增加了：源码路径校验、防止符号链接越界、严格 YAML 解析、强制源程序分页计划、PDF 渲染文本与页数审计、额外质量审查规则。**仍需人工审核最终 DOCX、PDF 及真实业务功能；不保证登记通过。**

## Codex 安装（Linux、macOS 或 WSL）

```bash
git clone https://github.com/llia731/copyright-forge-skill.git ~/.codex/copyright-forge-repo
mkdir -p ~/.codex/skills
ln -s ../copyright-forge-repo/skills/copyright-forge ~/.codex/skills/copyright-forge
python -m pip install pyyaml pymupdf reportlab
```

重新启动 Codex 会话，在待申请的软件项目根目录执行 `codex`，输入：

```text
$copyright-forge 请基于当前仓库分析真实功能，整理软著材料。
先确认软件范围和无法推断的申请事实，再生成 DOCX、PDF 与质量报告。
不要修改原仓库；最终文件按实际渲染结果核查。
```

更新：`git -C ~/.codex/copyright-forge-repo pull --ff-only`。

## 开发与核查

```bash
python -m pip install pyyaml pymupdf reportlab
python -m unittest discover -s tests -v
```

注意：现有源程序 PDF 生成器可能截断过长的代码行；必须使用新审计脚本并进行视觉检查，发现问题则修复或人工调整。自动测试不等于申报材料合规认证。

许可和来源：上游 [Copyright Forge Skill](https://github.com/Rodert/copyright-forge-skill)，Apache-2.0。规则需要依当前官方要求复核。
