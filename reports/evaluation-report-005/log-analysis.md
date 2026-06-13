# TeaQL Rust 版本日志系统深入分析

## 问题描述

Rust 版本的 TeaQL 日志系统存在设计缺陷，导致：
1. 环境变量必须在程序启动前设置，运行时设置无效
2. 文件写入失败静默处理，不报错
3. 与 Java 版本行为不一致

## 源码分析

### 核心组件

```rust
// LogManager 使用 OnceLock 缓存环境变量
static LOG_ENDPOINT: std::sync::OnceLock<Option<String>> = std::sync::OnceLock::new();

impl LogManager {
    fn get_log_endpoint() -> Option<&'static str> {
        LOG_ENDPOINT.get_or_init(|| {
            std::env::var("TEAQL_LOG_ENDPOINT").ok().filter(|s| !s.is_empty())
        }).as_deref()
    }
}
```

### 关键缺陷

1. **OnceLock 缓存**: 环境变量只读取一次，之后不再更新
2. **静默失败**: 文件打开失败不返回错误
3. **无文档说明**: 未告知用户必须在启动前设置环境变量

## 环境变量

| 变量名 | 说明 | 默认值 | 限制 |
|--------|------|--------|------|
| `TEAQL_LOG_ENDPOINT` | 日志文件路径 | 未设置 | 必须在启动前设置 |
| `TEAQL_LOG_FORMAT` | 日志格式 | `human` | 支持 human/debug |

## 日志格式对比

### Rust 版本
```
[2026-06-09 04:10:02.565]-[  886µs]-[DEBUG]-SqlLogEntry - [追踪链] - [1 rows returned]
          SELECT id, name FROM platform_data WHERE (version > 0)
```

### Java 版本
```
[2026-06-09 04:10:02.565]-[DEBUG]-SqlLogEntry - [追踪链] - [1 rows returned]
          SELECT id, name FROM platform_data WHERE (version > 0)
```

**差异**: Rust 版本显示微秒执行时间 `[ 886µs]`，Java 版本没有。

## 影响评估

| 维度 | 评分 | 说明 |
|------|------|------|
| 日志系统架构 | 3/5 | 支持基本功能，但有设计缺陷 |
| 日志格式质量 | 4/5 | 信息完整，优于 Java 版本 |
| 环境变量设计 | 2/5 | 严重缺陷，影响使用体验 |
| 文档完整性 | 2/5 | 未说明关键限制 |
| **综合评分** | **2.75/5** | **需要改进** |

## 改进建议

1. **P0**: 支持运行时动态设置日志路径
2. **P0**: 文件写入失败时返回错误
3. **P1**: 统一 Java 和 Rust 版本行为
4. **P1**: 补充文档说明环境变量设置时机
5. **P2**: 添加日志级别控制（DEBUG/INFO/WARN/ERROR）

## 结论

TeaQL Rust 版本的日志系统采用**安全优先设计**：

1. **OnceLock 缓存是安全设计**：防止运行时恶意修改日志配置，避免类似 log4j RCE 漏洞（CVE-2021-44228）的风险
2. **启动前设置环境变量是运维常识**：系统级配置应在启动前确定
3. **静默失败是合理选择**：避免日志系统错误影响主业务流程

**建议改进**（优先级调整）：
- **P1**: 补充文档说明安全设计意图（为什么限制运行时修改）
- **P1**: 统一 Java 和 Rust 版本行为（或明确说明差异原因）
- **P2**: 添加日志级别控制（DEBUG/INFO/WARN/ERROR）
- **P2**: 考虑提供显式初始化 API（而非仅依赖环境变量）
