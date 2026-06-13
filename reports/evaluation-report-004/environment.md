# 环境配置

## 硬件环境
- **操作系统**: macOS 12.6.8 (Monterey)
- **处理器**: Intel Core i7-4770HQ @ 2.2GHz
- **内存**: 16GB DDR3
- **存储**: SSD

## 软件环境
- **Rust 版本**: 1.94.1
- **Cargo 版本**: 1.94.1
- **TeaQL 版本**: 4.0.3
- **cargo-teaql 版本**: 0.2.0
- **数据库**: SQLite (通过 teaql-provider-sqlx-sqlite 3.2.3)

## 网络环境
- **代理**: http://192.168.1.1:1087
- **TeaQL 服务端**: http://t420.doublechaintech.cn:23380
- **GitHub 访问**: 通过 personal access token

## 项目配置

### Cargo.toml 依赖
```toml
[dependencies]
teaql-core = "4.0.3"
teaql-runtime = "4.0.3"
teaql-sql = "4.0.3"
teaql-provider-sqlx-sqlite = "3.2.3"
teaql-macros = "4.0.3"
tokio = { version = "1", features = ["full"] }
```

### 环境变量
```bash
TEAQL_AUDIT=production
TEAQL_SCHEMA=execute
TEAQL_SQL_LOG=off
```

## 工作目录
- **A-001**: `/Users/openclaw-002/workspace/A-001/` - 首次评估（含补丁）
- **A-002**: `/Users/openclaw-002/workspace/A-002/` - 完整评估（autonomous 分支）
- **A-003**: `/Users/openclaw-002/.qclaw/workspace/A-003/` - API 演示

## 工具链
- **代码生成**: `cargo teaql generate`
- **模型验证**: `cargo teaql eval`
- **构建**: `cargo build`
- **测试**: `cargo test`
- **运行**: `cargo run`

## 已知限制
- 编译周期：4-8 分钟（依赖解析 + 代码生成）
- 内存占用：编译时约 2-4GB
- 磁盘空间：生成代码约 5MB，编译产物约 500MB
