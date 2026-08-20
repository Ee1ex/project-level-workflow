# Eelex Blog Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有 `Eelex Journal / Eelex Code Hub` 的正式产品身份统一为 `Eelex Blog`，并准备把 GitHub 仓库改名为 `eelex-blog`。

**Architecture:** 只修改单一站点品牌常量、依赖该常量的 SEO/页面壳、README 和 npm workspace 包名；不重做组件结构、视觉系统、路由、内容或部署。所有开发发生在从 `main@ce22d7d` 创建的隔离工作树中，现有脏工作树的 `.codex/` 与 `public/eelex-avatar.png` 不进入分支。

**Tech Stack:** Next.js 16、React 19、TypeScript 6、Vitest、pnpm 11、Prettier、ESLint。

## Global Constraints

- 正式展示名为 `Eelex Blog`，目标仓库为 `Ee1ex/eelex-blog`，包名为 `eelex-blog`。
- 只改品牌和仓库身份，不改视觉设计、路由、域名、内容架构或部署平台。
- 从 `origin/main@ce22d7d77435e803063f415651da8ceb9ef0c620` 创建 `codex/eelex-blog-rename` 隔离工作树。
- 现有 `.codex/` 与 `public/eelex-avatar.png` 不修改、不移动、不删除、不提交。
- 不执行 GitHub 仓库改名、Push、PR 或部署，直到用户再次明确确认。
- 所有文件编辑使用 `apply_patch`；每个任务遵循失败测试、最小实现、相关测试、Diff 检查、本地提交。

---

### Task 1: 建立 `Eelex Blog` 品牌合同

**Files:**
- Modify: `tests/seo.test.ts`
- Modify: `tests/app-shell.test.tsx`
- Modify: `tests/page-shells.test.tsx`
- Modify: `tests/engineering-config.test.ts`

**Interfaces:**
- Consumes: `src/site/seo.ts` 导出的 `siteName` 和 `createPageTitle(title)`。
- Produces: 页面、SEO、页头页尾和包名必须满足的失败合同。

- [ ] **Step 1: 修改 SEO 期望**

在 `tests/seo.test.ts` 将正式名称断言统一为：

```typescript
expect(seo?.siteName).toBe("Eelex Blog");
expect(seo?.createPageTitle("关于我")).toBe("关于我 | Eelex Blog");
expect(HomePage.metadata).toMatchObject({
  title: "Eelex Blog",
  description: "一个关于代码、设计与学习的个人空间。",
});
expect(metadata).toMatchObject({
  title: "让界面更易阅读的三个小决定 | Eelex Blog",
});
```

- [ ] **Step 2: 修改页面壳和包名期望**

在 `tests/app-shell.test.tsx` 断言：

```typescript
expect(markup).toContain("© 2026 Eelex Blog");
expect(markup).not.toContain("Eelex Code Hub");
```

在 `tests/page-shells.test.tsx` 增加页头断言：

```typescript
expect(header).toContain("Eelex Blog");
expect(header).not.toContain("Eelex Code Hub");
```

在 `tests/engineering-config.test.ts` 增加：

```typescript
const pkg = JSON.parse(readFileSync(resolve(process.cwd(), "package.json"), "utf8"));
expect(pkg.name).toBe("eelex-blog");
```

复用文件已有的 `node:fs` / `node:path` import；若不存在，只增加 `readFileSync` 与 `resolve`。

- [ ] **Step 3: 运行测试并确认失败**

Run: `corepack pnpm vitest run tests/seo.test.ts tests/app-shell.test.tsx tests/page-shells.test.tsx tests/engineering-config.test.ts`

Expected: FAIL，实际名称仍为 `Eelex Code Hub`，包名仍为 `eelex-journal`。

- [ ] **Step 4: 检查并提交测试合同**

Run: `git diff --check`

Stage only: `tests/seo.test.ts tests/app-shell.test.tsx tests/page-shells.test.tsx tests/engineering-config.test.ts`

Commit: `test: define Eelex Blog brand contract`

### Task 2: 最小实现站点和包品牌改名

**Files:**
- Modify: `src/site/seo.ts`
- Modify: `src/components/site-header.tsx`
- Modify: `src/components/site-footer.tsx`
- Modify: `package.json`

**Interfaces:**
- Consumes: Task 1 的品牌合同。
- Produces: `siteName = "Eelex Blog"`，页面壳只显示新品牌，workspace 包名为 `eelex-blog`。

- [ ] **Step 1: 修改单一 SEO 品牌常量**

在 `src/site/seo.ts` 使用：

```typescript
export const siteName = "Eelex Blog";
```

保持 `defaultDescription`、`siteUrl`、`createPageTitle` 和 `toAbsoluteUrl` 逻辑不变。

- [ ] **Step 2: 修改页头与页尾可见名称**

在 `src/components/site-header.tsx` 和 `src/components/site-footer.tsx` 将所有作为站点正式名称的 `Eelex Code Hub` 改为 `Eelex Blog`。保留“关于 Eelex”等作者身份文本。

- [ ] **Step 3: 修改包名**

在 `package.json` 精确改为：

```json
"name": "eelex-blog"
```

不改版本、依赖、脚本、Node 或 pnpm 版本。

- [ ] **Step 4: 运行相关测试**

Run: `corepack pnpm vitest run tests/seo.test.ts tests/app-shell.test.tsx tests/page-shells.test.tsx tests/engineering-config.test.ts`

Expected: PASS。

- [ ] **Step 5: 检查并提交**

Run: `git diff --check`

Stage only: `src/site/seo.ts src/components/site-header.tsx src/components/site-footer.tsx package.json`

Commit: `feat: rename the site to Eelex Blog`

### Task 3: 更新 README 和治理记录

**Files:**
- Modify: `README.md`
- Create: `docs/REQ-20260820-06-eelex-blog-rename.md`
- Create: `docs/DEV-20260820-03-eelex-blog-rename.md`
- Modify: `docs/PROG-20260820.md`
- Modify: `tests/engineering-config.test.ts`

**Interfaces:**
- Consumes: Task 2 的最终显示名和包名。
- Produces: 新仓库名称、范围、验证、回滚和未验证项的可追溯记录。

- [ ] **Step 1: 增加 README 失败合同**

在 `tests/engineering-config.test.ts` 增加：

```typescript
const readme = readFileSync(resolve(process.cwd(), "README.md"), "utf8");
expect(readme).toContain("# Eelex Blog");
expect(readme).not.toContain("Eelex Code Hub");
expect(readme).toContain("Ee1ex/eelex-blog");
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `corepack pnpm vitest run tests/engineering-config.test.ts`

Expected: FAIL，README 仍使用旧名称且未记录目标仓库。

- [ ] **Step 3: 更新 README**

README 首行使用：

```markdown
# Eelex Blog
```

首段改为“Eelex Blog 是一个以中文记录代码、界面设计与持续学习的个人博客”。截图 alt 同步使用 `Eelex Blog`。增加仓库链接：

```markdown
[GitHub 仓库](https://github.com/Ee1ex/eelex-blog)
```

- [ ] **Step 4: 写需求、实现和进度记录**

`docs/REQ-20260820-06-eelex-blog-rename.md` 必须记录：目标、范围、不做项、用户未跟踪文件保护、远程改名 Gate 和 DoD。

`docs/DEV-20260820-03-eelex-blog-rename.md` 必须记录：受影响文件、测试命令、实现决策、仓库改名步骤、回滚和待验证项。

在 `docs/PROG-20260820.md` 追加一条链接到上述 REQ/DEV 的结构化进度记录，不重写历史条目。

- [ ] **Step 5: 运行相关测试并提交**

Run: `corepack pnpm vitest run tests/engineering-config.test.ts tests/seo.test.ts tests/app-shell.test.tsx tests/page-shells.test.tsx`

Expected: PASS。

Run: `git diff --check`

Stage only: `README.md docs/REQ-20260820-06-eelex-blog-rename.md docs/DEV-20260820-03-eelex-blog-rename.md docs/PROG-20260820.md tests/engineering-config.test.ts`

Commit: `docs: document the Eelex Blog rename`

### Task 4: 完成全量验证和远程改名准备

**Files:**
- Modify: `docs/DEV-20260820-03-eelex-blog-rename.md`

**Interfaces:**
- Consumes: Tasks 1–3 的完整本地改名。
- Produces: 可供用户批准 GitHub 仓库改名、Push 和 PR 的真实证据。

- [ ] **Step 1: 运行完整质量门**

Run: `corepack pnpm check`

Expected: Prettier、Next typegen、TypeScript、ESLint、Vitest 和 Next build 全部退出 0。不得把未运行的平台或浏览器检查写成通过。

- [ ] **Step 2: 检查旧正式名称残留**

Run: `rg -n "Eelex Code Hub|Eelex Journal|eelex-journal|Eelex-Journal" README.md package.json src tests`

Expected: 无输出。历史治理文档不做全局替换。

- [ ] **Step 3: 验证用户改动隔离**

在原工作树 `D:\VibeCoding-Project\Eelex-Journal` 运行：

```text
git status --short --branch
```

Expected: `.codex/` 与 `public/eelex-avatar.png` 仍为原有未跟踪状态；隔离分支提交不包含它们。

- [ ] **Step 4: 运行 Diff 检查**

Run: `git diff origin/main...HEAD --check`

Expected: 无输出、退出码 0。

- [ ] **Step 5: 回写真实证据并提交**

把 `corepack pnpm check` 的实际结果、测试数量、构建结果、旧名称扫描、原工作树保护证据、未验证项和回滚写入 `docs/DEV-20260820-03-eelex-blog-rename.md`。

Stage only: `docs/DEV-20260820-03-eelex-blog-rename.md`

Commit: `docs: record Eelex Blog rename readiness`

完成后停止并提供：分支、提交、文件范围、测试证据、目标仓库名 `eelex-blog`、PR 方案、Merge 方式、回滚和未验证项。GitHub 仓库改名、Push 和 PR 创建必须再次确认并在完成后回读验证。
