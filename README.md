# My prject

第一件事，请把 代码中，所有的 **diting** 替换成真实的项目名称

Please modify diting in the prject

## Usage

### 生产启动命令

```bash
# 切换到src 目录
cd src/
```

```bash
sanic --host=0.0.0.0 --port=8000 --worker=1 diting.server.app
```

### 调试启动

```bash
python -m sanic --dev diting.server.app
```

### vscode 调试

前提条件，ddd-structure 是vscode 打开的顶层目录

新建 .vscode 目录

在launch.json 文件中【无则新建一个】，贴入以下内容

```json
{
    // 使用 IntelliSense 了解相关属性。
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [{
            "name": "Python: 模块",
            "type": "python",
            "request": "launch",
            "module": "sanic",
            "args": ["diting.server.app"],
            "cwd": "${cwd}/src",
            "justMyCode": false
        }
    ]
}
```

### 本地开发环境的配置文件
1. 新建 src/diting/settings-dev.toml
2. 写入需要调整的配置


### swagger

配置文件中，我添加了PATH 装饰，会将路径前自动拼接上项目绝对路径



```
127.0.0.1:8000/docs
or
127.0.0.1:8000/docs/swagger
of
127.0.0.1:8000/docs/redoc

```

### 配置文件中加密说明

settings.toml 文件中，值为 ENC(.*) 范式的，则说明是需要进行加解密支持的

#### 密钥

settings.toml 中的 secret_key， 内部代码封装是，会自动生成 encode_secret_key, 本应用内用户无需关心 encode_secret_key。 但若是跨应用使用，则给对方 encode_secret_key

**切记：字符串用 单引号 包围**

#### encode_secret_key 生成命令

```bash
cd src/diting/core/common
python crypto.py -a generate -d 'YOUR_SECRET_KEY'
```

#### 加密命令

```bash
cd src/diting/core/common
python crypto.py -a encrypt -d 'YOUR_NEED_ENCRYPT_DATA' -k 'YOUR_SECRET_KEY'

```

#### 解密命令

```bash
cd src/diting/core/common
python crypto.py -a decrypt -d 'YOUR_ENCRYPTED_DATA' -k 'YOUR_SECRET_KEY'
```

### 数据库初始化（alembic）

1. alembic.ini 中，配置 sqlalchemy 的连接串
2. alembic/env.py 中，添加target_metadata

初始化命令：

```bash
# 切换到和 alembic.ini 同一级的目录
cd src/diting

# 生成变化
alembic revision --autogenerate -m "init db"

# 执行变更
alembic upgrade head

# 降级
alembic downgrade XXXX
```
