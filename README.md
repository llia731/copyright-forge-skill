# Copyright Forge Skill

面向中国软件著作权登记材料准备的 Agent Skill。基于真实软件项目整理**源码证据、源程序鉴别材料、软件说明书、申请表填写参考和审核记录**。

本仓库为 [Rodert/copyright-forge-skill](https://github.com/Rodert/copyright-forge-skill) 的独立改进版本，保留 [Apache-2.0 许可证](LICENSE)。**不是官方登记系统，不代替权属审查，也不保证登记通过。**

## 使用范围

| 本仓库负责 | 本仓库不保存、不代替 |
| --- | --- |
| 通用 Agent Skill、工作流程和提示词 | 某个公司的申请表、软件说明书和申请人信息 |
| 源码收集、证据映射、交存材料生成工具 | 真实业务代码、数据库、内部地址和访问密钥 |
| 申请信息模板、核查规则与写作规范 | 官方登记申请表、申请人签章、权属证明 |
| 跨项目复用的安全检查与测试 | 以生产部署、算法性能实验作为普通登记的固定前提 |

项目专属资料应放在**独立的私有材料仓库**。本仓库是公共技能工具，不是申报项目工作区。详见 [仓库分工与资料边界](docs/repository-boundaries.md)。

## 安装（Codex，Linux、macOS 或 WSL）

```bash
git clone https://github.com/llia731/copyright-forge-skill.git ~/.codex/copyright-forge-repo
mkdir -p ~/.codex/skills
ln -s ../copyright-forge-repo/skills/copyright-forge ~/.codex/skills/copyright-forge
python -m pip install pyyaml pymupdf reportlab
```

重新启动 Codex，在待分析的软件项目根目录运行：

```text
$copyright-forge 根据当前源码整理软件著作权申报材料。
请核对功能对应的代码证据，列出不能从源码确认的权属事实。
不要修改原始项目，不要写入密钥；核查交存页及最终文档的实际排版。
```

更新技能：`git -C ~/.codex/copyright-forge-repo pull --ff-only`。

## 仓库目录

```text
copyright-forge-skill/
├── skills/copyright-forge/
│   ├── SKILL.md                技能入口与任务分流
│   ├── prompts/                创建、审阅、继续和补正流程
│   ├── references/             核查口径、官方资料索引和写作规范
│   ├── assets/                 通用模板和结构化数据格式
│   └── scripts/                源码分析、交存生成和质量检查
├── docs/                       结构说明、仓库分工和维护规范
└── tests/                      工具回归测试和样例项目
```

完整文件导航见 [docs/README.md](docs/README.md)，技能的具体调用规则见 [SKILL.md](skills/copyright-forge/SKILL.md)。

## 审核原则

- 功能文字以待登记的软件版本为准。当前代码与历史压缩包不同时，应先核对快照；不能用旧代码证明新功能。
- 软件著作权登记的**法定材料要求**和软件工程质量改进的**建议检查**应分开。不要把生产环境、业务数据、复杂算法评测作为普通登记的统一硬性要求。
- 软件名称、权利人、开发完成日期、发表状态、权属来源等不能从代码推断；申请人确认后再写入正式材料。
- 交存源程序与文档应检查实际页数、代码行数、版式、安全和版本一致性；自动检查通过不等于官方受理。
- AI 参与代码、文档或申报材料时必须如实保留事实，不以改写文风代替诚信声明核查。

## 本地开发与测试

```bash
python -m pip install pyyaml pymupdf reportlab
python -m unittest discover -s tests -v
```

现有源程序 PDF 生成器可能截断过长代码行，应结合 `audit_rendered_pdf.py` 和目视检查，不可只依据逻辑分页结果判定质量。官方申请要求随时间变化，应在提交时依据办理系统再次核实。

## 来源与许可

- 上游：[Copyright Forge Skill](https://github.com/Rodert/copyright-forge-skill)
- 许可：[Apache-2.0](LICENSE)
- 开发安全：[SECURITY.md](SECURITY.md)
- 维护记录：[CHANGELOG.md](CHANGELOG.md)
