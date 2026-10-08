# PRD — AI 知识库（Agent 版）

> 版本：v1.1 ｜ 日期：2026-08-15 ｜ 读者：Agent（接管/协作者）
> 本文档是 Agent 的工作手册：完整上下文、设计决策、技术细节、踩坑记录、生产流程。
> 人类阅读版见 `PRD-人类版.md`；内容规范见 `CONTENT-SPEC.md`；唯一事实源 `DESIGN-SPEC.md`。

---

## 一、项目定位与核心价值

**一句话**：一线知识的沉淀与导航站——开源、Wiki 式、面向所有人的 AI 知识库。

**解决的问题**：
- 社区内容永远跑在正式知识前面（GitHub/推文/论文预印本 → 大 V 解读 → 教程 → Wiki 词条，滞后 6-12 个月）
- 现有 AI 术语站要么词条少（vibehub 纯 JS 空壳）、要么单页堆砌（无独立词条页）、要么过气
- 用户需要"从底层原理长出来"的知识树，而非散装词条

**四根柱子**（产品哲学，所有决策的底层依据）：

| 柱子 | 含义 | 机制 |
|------|------|------|
| 上限 | 内容能多深、多新、多一线 | 靠来源层级，每词条带原始链接 |
| 标准 | 多规范、多可信、多一致 | 靠 Schema 校验 + 无源不收录 |
| 生态 | 内容产品活着 | 靠开放编写（四层贡献模型） |
| 信任 | 读者凭什么信 | 靠 git 留痕 + 来源标注 + 修订记录 |

---

## 二、核心设计决策（含决策理由）

### 2.1 知识树结构：词条是节点，关系是边

- 每个词条一个 `.md` 文件，frontmatter 带坐标（dimension/granularity）+ 关系（relations）
- **垂直**：粒度链（dimension 相同，granularity 递进）—— 厂商 → 模型家族 → 变体
- **水平**：平行组（dimension + granularity 都相同）—— 同层兄弟词条，可对比可并列
- **[注意] 用户纠正过的认知**：目录拆分 ≠ 分裂。Wiki 是网状不是树状，目录只是导航索引，同一概念多处入口是正常的（如 llama.cpp 同时在"工具"和"框架与库"）。不要"清理重复"。

### 2.2 渲染原则：结构在代码层，文字给读者（[重要] 核心）

- frontmatter（dimension/granularity/relations）是代码层的坐标与路由，给机器和 Agent 用
- **渲染出来的页面必须是干净的人话文章**（像 Wikipedia）：标题 → 正文（定义/原理/历史/应用）→ 文末"参见"自然链接
- 不渲染：关系表格、类型标签、坐标面板、成熟度徽章（[热词] 热词警示条除外——必须显示）
- **[注意] 用户明确抱怨过**：装饰字符（◆● 等 CSS content 注入）渲染成奇怪符号（曾被误认为"圆形感叹号"），禁止使用。emoji 只放标题文字前，不用 CSS 注入。

### 2.3 关系（relations）：语义接近即链接

- 必填：`target`（指向哪个词条）+ `note`（一句话说明为什么接近——给读者看，也是未来机器学习路径的原料）
- 可选：`type`（prerequisite/part_of/peer/contrast/evolved_from/applies_to/similar_to），不标不校验
- **本质**：relations = 语义接近度的显式声明。关系模糊是常态，硬分类反而失真（用户拍板简化）
- 规则：一个词条没有 relations = 孤岛，不合格

### 2.4 渐进披露：树根写全，树叶挂链

- **树根（01-底层原理）**：写全——历史 + 原理 + 应用各 2-4 段
- **枝（02-组件）**：原理 2-4 段 + 应用结合 ComfyUI 实际
- **叶（03+）**：原理只写 2-3 句 + 链到底层词条（如 `[量化](../../01-底层原理/量化.md)`），不重复展开
- 目的：读者想深挖自己爬树，想速查看叶子，篇幅可控

### 2.5 成熟度分级

- [稳定] stable（已沉淀）：完整定义 + 多源交叉验证
- [热词] hot（社区热词）：一句话定义 + 单一来源 + **必须**标注「[热词] 社区热词，未经沉淀，信息可能快速过时」（一字不能少）
- 升级规则：hot → stable 需 ≥2 个独立来源 + 维护者审校

### 2.6 三阶段演进（用户明确的方向）

```
阶段 1（现在）：纯静态 + Agent 生产 —— 内容 = Agent 预生成 md → 静态部署
阶段 2（共创初期）：静态 + GitHub 原生协作 —— Issue（纠错/讨论）+ PR（提交词条），GitHub 就是免费动态层
阶段 3（共创规模化）：才需要真后端 —— 用户体系/站内评论/实时搜索
```

**架构约束**：内容必须保持 md 文件（GitHub 协作载体 + 未来数据源）；不急着上数据库/服务器（会变负担）。GitHub 的 Issue/PR/Discussions 是现成的动态交互层。

---

## 三、技术架构

### 3.1 栈

| 层 | 选择 | 理由 |
|---|---|---|
| 静态生成 | MkDocs + Material 主题 | md 原生、目录结构自动生成侧边栏树（文件树=知识树）、内置搜索/暗色模式 |
| 部署 | GitHub Pages + Actions | 零成本、push 即上线、CDN 全球加速 |
| 内容 | Markdown + YAML frontmatter | GitHub 协作天然载体 |
| 素材库 | `采集/采集/`（1.35MB HF 课程 + 社区底料） | 内容不靠训练数据 |
| 生产 | Agent 协作（Hermes 编排 + Kimi/Claude Code） | 生产单是 Agent 无关的 |

### 3.2 目录结构（知识树物理实现）

```
docs/
├── index.md               # 首页（hero + 知识树 + 导航）
├── 项目文档/              # CONTENT-SPEC / CONTRIBUTING / MAINTENANCE / DESIGN-SPEC
├── stylesheets/extra.css  # HF 风格主题
└── 词条/
    ├── 01-底层原理/       # 树根（8 个）
    ├── 02-组件/           # 枝（7 个）
    ├── 03-表层概念/       # 叶（~45 个）：量化格式/微调/加速/LLM/Agent/对齐/模型厂商/模型家族/工具
    ├── 04-LLM工程/        # LLM 落地（7 个骨架）
    ├── 05-Agent工程/      # Agent 开发（6 个骨架）
    └── 06-IT行业/         # 地基（20 个骨架）：编程语言/操作系统/基础设施 + 框架与库
```

### 3.3 关键配置文件

- `mkdocs.yml`：Material 主题、primary orange / accent pink（HF 色）、mermaid2 插件、中文搜索
- `docs/stylesheets/extra.css`：深色星空底 + HF 多彩体系（主橙 #FF9D0B / 粉 #FF0789 / 黄 #FFD21E / 绿 #21DE75）
- `.github/workflows/deploy.yml`：pip install mkdocs-material → mkdocs build → upload-pages-artifact → deploy-pages

### 3.4 构建与部署

```bash
# 本地构建（用 Python 3.14，注意 pip 装到了 pythoncore-3.14）
"C:/Users/A/AppData/Local/Python/pythoncore-3.14-64/python.exe" -m mkdocs build
# strict 模式验证死链（提交前必跑）
"...python.exe" -m mkdocs build --strict

# git 推送（[注意] 必须用 HTTP/1.1，仓库级已配置）
git push origin main
```

---

## 四、内容生产流程（Agent 用）

### 4.1 生产单模式

1. 写 `词条生产单-第X批-主题.md`：每个词条的 term/category/dimension/granularity/要点/relations 声明
2. 写 `.kimi-prompt-词条X.txt` 或 `.claude-prompt`：引用规范 + 生产单 + 素材库
3. 后台跑 Agent（`background=true, notify_on_complete=true`）
4. **独立验证**（不信 Agent 自述）：
   - 文件存在性 + frontmatter 14 字段齐全
   - 正文五区（定义/原理/由来与历史/应用/参见）齐全
   - relations ≥3 且 target+note 必填
   - 表层概念渐进披露（原理 150-250 字 + 链底层）
   - hot 词条有警示条
5. `mkdocs build --strict` 验证死链
6. commit + push

### 4.2 Agent 切换（Kimi OAuth 故障记录）

- Kimi Code 是"云认证"架构：token 15 分钟过期，过期需连 auth.kimi.com 刷新
- **故障案例**：Clash fake-ip 劫持 auth.kimi.com DNS → 代理规则未放行 → CLI 认证死路。修复：hosts 钉真实 IP（`103.143.17.156 auth.kimi.com`）
- 生产单是 Agent 无关的，Claude Code 可用 `claude -p "$(cat prompt)" --allowedTools "Read,Write,Edit,Glob,Grep" --max-turns 40` 顶替
- Kimi 恢复后 hosts 方案已验证生效

### 4.3 素材库（采集/采集/）

| 目录 | 内容 | 大小 |
|---|---|---|
| hf-diffusion-course/ | HF 官方扩散课程 | 973KB |
| hf-courses/ | 11 门课程（LLM/Agent/Context/RL...） | 380KB |
| 各种 .md | 社区采集（GitHub issues 底料） | 6KB |

**HF 采集方法**：`robots.txt` 完全放行，课程有 `.md` 端点（`/learn/<course>/<unit>.md`）直接返回纯 Markdown。慢速采集（1-1.5s 间隔）。脚本 `scripts/hf_courses_collect.py`。

---

## 五、踩坑记录（重要！）

1. **Git push 卡死**：代理对 GitHub HTTP/2 长连接不稳 → 仓库级配置 `http.version=HTTP/1.1` + `http.lowSpeedLimit/Time`，已写入 `.git/config`，勿删
2. **Jekyll 残留覆盖**：Pages 从 legacy Jekyll 切 Actions 后，旧 Jekyll 构建竞争部署 → 手动触发 workflow_dispatch 后 CDN 刷新才生效
3. **md-status 灰色圆圈**：MkDocs Material 给每词条自动加的"已发布"状态图标（读者困惑）→ CSS `.md-status { display: none }` 隐藏
4. **中文路径 404**：curl 直接传中文 URL 会乱码，需 URL 编码；Python urllib 用 `urllib.parse.quote`
5. **pip 版本错位**：`pip` 指向 Python 3.14，`python` 指向 3.11 venv。mkdocs 用 3.14 完整路径调用
6. **装饰字符禁令**：用户明确反感 ◆● 等 CSS content 注入（渲染成奇怪符号）
7. **死链批量修复**：词条在子目录（模型家族/模型厂商 二层深）时，相对路径容易错。规则：指向 01/02 用 `../../`，指向 03 同层用 `../`。修复后必须 `build --strict` 验证

---

## 六、当前状态（2026-08-14）

- [OK] 110 词条（88 完整 + 22 骨架），6 大类知识树
- [OK] 前端 HF 风格（深色星空 + 橙粉多彩）
- [OK] 素材库 1.35MB
- [OK] strict 构建 0 警告 0 死链
- [OK] 索引页 6 大类导航
- ⏳ 骨架词条细节填充（22 条待补）
- ⏳ 「文章与引用」栏目（MOKE 调研完成，见 `采集/调研-MOKE文章引用栏目.md`）
- ⏳ 采集 cron 自动化
- ⏳ 网络修复（整体依赖代理，hosts 临时方案已生效）

## 七、下一步建议（按优先级）

1. **「文章与引用」栏目**：`docs/文章与引用/`（索引 + 聚合 + 引用库），模式 = MOKE 的「聚合摘要 + 判断线索 + 阅读索引」，引用挂到词条 relations
2. **骨架细节填充**：优先 04-LLM工程 / 05-Agent工程（新方向）
3. **采集 cron**：定时扫 arXiv/GitHub/HF → 热词卡 → 采集/ 目录
4. **网络修复根治**：整体依赖代理问题

## 八、给接手 Agent 的注意事项

- 先读 DESIGN-SPEC.md（唯一事实源）+ CONTENT-SPEC.md（内容规范）再动手
- 用户偏好：中文回复、人话优先、渐进披露、技术决策自主但内容决策需确认
- 用户纠正过的认知必须遵守：目录≠分裂、关系=语义接近、结构在代码层文字给读者、先框架后细节
- 每个新词条必须声明 relations（无关系=孤岛=不合格）
- 提交前跑 `mkdocs build --strict`（死链=0 是硬要求）
