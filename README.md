# TeaQL 总览

TeaQL 是一套围绕领域模型、代码生成和类型安全查询 API 的开发体系。它的核心目标是：

- 用紧凑的领域模型描述业务对象、字段、关系和行为。
- 生成接近自然语言的强类型查询 API，减少手写 Repository 和样板代码。
- 支持关系图查询、关系增强、聚合统计、图保存和安全表达式访问。
- 在 Java 体系的经验基础上，逐步形成 Rust 原生运行时和生成器。

这个仓库作为 TeaQL 多项目的总入口，记录整体说明、仓库列表、阅读顺序和当前整理状态。

## 当前主线

TeaQL 目前有两条主要技术线：

1. **Rust 新主线**

   Rust 版本把 TeaQL 拆成运行时、SQL 编译、宏、方言、生成器和 CLI。当前重点是 `teaql-rs`、`teaql-code-gen` 和 `teaql-cli`。

2. **Java / Spring Boot 既有体系**

   Java 版本包含 Spring Boot starter、项目模板、示例服务、生成服务和历史工具项目。它承载了 TeaQL 早期的设计和应用经验。

## 核心项目

| 项目 | 定位 | 主要技术 | 远端 |
| --- | --- | --- | --- |
| `teaql-rs` | Rust 原生 TeaQL 运行时，包含 entity metadata、query AST、SQL 编译、repository、graph save、checker、event、PG/SQLite executor 等 | Rust / Cargo | <https://github.com/teaql/teaql-rs.git> |
| `teaql-code-gen` | TeaQL 代码生成服务，把领域模型生成 Java 或 Rust 库；Rust `rust-lib` 已是一等目标 | Java / Gradle / Spring Boot / StringTemplate | <https://github.com/teaql/teaql-code-gen.git> |
| `teaql-cli` | Rust CLI，封装生成代码、生成文档、生成模型、配置和本地命令别名 | Rust / Cargo | <https://github.com/teaql/teaql-cli.git> |
| `teaql-spring-boot-starter` | Java / Spring Boot 集成入口，支撑旧版 TeaQL 服务项目 | Java / Gradle / Spring Boot | <https://github.com/teaql/teaql-spring-boot-starter.git> |

## 工具和界面项目

| 项目 | 定位 | 主要技术 | 远端 |
| --- | --- | --- | --- |
| `teaql-io-site` | TeaQL 官网和文档站点 | Docusaurus / Node | <https://github.com/teaql/teaql-io-site.git> |
| `teaql-database-design` | 数据库/模型设计前端，当前 README 仍是 Bun 模板说明，需要补齐产品定位 | Bun / React | <https://github.com/teaql/teaql-database-design.git> |
| `teaql-modeling-studio` | TeaQL 建模工作台，当前 README 很薄，需要补齐功能说明 | 前端项目 | <https://github.com/teaql/teaql-modeling-studio.git> |
| `teaql-editor` | 面向 TeaQL 的编辑器工具 | 编辑器工具 | <https://github.com/teaql/teaql-editor.git> |
| `teaql-local-agent` | 本地 agent / 服务编排入口，连接 LLM、TeaQL 生成服务和构建服务 | Java / Docker | <https://github.com/teaql/teaql-local-agent.git> |

## 模板、示例和实验项目

| 项目 | 定位 | 主要技术 | 远端 |
| --- | --- | --- | --- |
| `teaql-project-template` | Java TeaQL 服务项目模板 | Java / Gradle / Spring Boot | <https://github.com/teaql/teaql-project-template.git> |
| `teaql-demo-service` | TeaQL 示例服务，包含 `models/main.xml` 和 Spring Boot 构建文件 | Java / Maven / Spring Boot | 未配置 origin |
| `teaql-todo-list` | 早期 app template / todo 示例 | Java / TeaQL | <https://github.com/philipgreat/teaql-todo-list.git> |
| `teaql-lib-gen-with-actions` | 生成 TeaQL library 的实验项目 | 生成工具实验 | <https://github.com/teaql/teaql-lib-gen-with-actions.git> |
| `teaql-git-server` | 基于 Spring Boot 的 Git HTTP 服务实验 | Java / Gradle / Spring Boot | <https://github.com/philipgreat/teaql-git-server.git> |
| `teaql-auto-complete` | 早期自动补全脚本/实验项目 | Shell | 未配置 origin |
| `teaql-local-agent-bak` | `teaql-local-agent` 的备份目录 | 历史备份 | 未配置 origin |

## 推荐阅读顺序

面向 Rust 主线：

1. `teaql-rs/README.md`：理解当前 Rust runtime 的边界、crate 拆分和能力清单。
2. `teaql-code-gen/README.md`：理解领域模型如何生成 Rust service crate，以及生成出来的 `Q`、`E`、entity、behavior 和 module。
3. `teaql-cli/README.md`：理解命令行如何调用生成流程。
4. 生成一个示例库后，再回到 `teaql-rs` 看 executor、repository、graph save 和 relation enhancement。

面向 Java / Spring Boot 体系：

1. `teaql-spring-boot-starter`
2. `teaql-project-template`
3. `teaql-demo-service`
4. `teaql-code-gen` 中 Java generator 相关模块

面向产品和文档：

1. `teaql-io-site`
2. `teaql-database-design`
3. `teaql-modeling-studio`
4. `teaql-editor`
5. `teaql-local-agent`

## TeaQL 查询风格示例

TeaQL 的目标 API 风格是用可读的强类型链式调用表达查询、关系加载和统计。

```java
Q.families()
```

```java
Q.families().selectKidList()
```

```java
Q.families().hasKids(Q.kids().whosGenderIsBoy())
```

```java
Q.families().countKids("kidGirlsCount", Q.kids().whosGenderIsGirl())
```

Rust 新主线的生成 API 也延续这个方向：

```rust
use crm_erp_service::Q;

let platforms = Q::platforms()
    .select_merchant_list_with(
        Q::merchants()
            .select_name()
            .which_names_contain("TeaQL"),
    )
    .execute_for_list(&ctx)
    .await?;
```

## 本地仓库状态快照

以下状态来自 2026-05-12 本地 `~/githome`：

| 项目 | 分支 | 本地变更数 | 备注 |
| --- | --- | ---: | --- |
| `teaql` | `main` | 0 | 总入口仓库 |
| `teaql-rs` | `master` | 5 | Rust runtime 主线，有本地未提交变更 |
| `teaql-code-gen` | `main` | 8 | 生成器主线，有本地未提交变更 |
| `teaql-cli` | `main` | 4 | CLI，有本地未提交变更 |
| `teaql-spring-boot-starter` | `main` | 1 | Java starter，有本地未提交变更 |
| `teaql-io-site` | `2026-05-11-refine-blog` | 0 | 文档站点当前在专题分支 |
| `teaql-database-design` | `main` | 1 | README 仍为模板说明 |
| `teaql-modeling-studio` | `main` | 1 | README 待补齐 |
| `teaql-editor` | `main` | 0 | README 较简 |
| `teaql-local-agent` | `main` | 6 | 有本地未提交变更 |
| `teaql-project-template` | `master` | 0 | Java 项目模板 |
| `teaql-git-server` | detached / unknown | 59 | README 存在 Git 冲突标记，需要优先清理 |
| `teaql-lib-gen-with-actions` | `main` | 1 | 实验项目 |
| `teaql-todo-list` | `main` | 1 | 示例/模板项目 |

## 待整理事项

- 给每个仓库补齐统一格式的 README：定位、运行方式、测试方式、发布方式、依赖关系。
- 清理 `teaql-git-server/README.md` 中的冲突标记。
- 明确哪些仓库是主线维护，哪些仓库是历史归档或实验项目。
- 为 Rust 主线补一张端到端流程图：model XML -> code generator -> generated service crate -> teaql-rs runtime -> database。
- 将 Java 体系和 Rust 体系的能力差异整理成迁移说明。
- 为 `teaql-database-design`、`teaql-modeling-studio`、`teaql-editor` 补充产品边界，避免工具项目含义重叠。
