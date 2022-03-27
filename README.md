# My prject

第一件事，请把 代码中，所有的 **myproject** 替换成真实的项目名称

Please modify myproject in the prject

## Usage

### 生产启动命令

```bash
# 切换到src 目录
cd src/
```

```bash
sanic --host=0.0.0.0 --port=7777 --worker=1 myproject.server.create_app
```

### 调试启动

```bash
python -m sanic --dev myproject.server.app
```

### swagger

san-ext 中，swagger 需要连接一个cdn, 请直接使用我修改的代码：

git clone https://github.com/SheldonXLD/sanic-ext.git

python setup.py install

```
http://localhost:7777/docs/swagger

```

### 配置文件中加密说明

settings.toml 文件中，值为 ENC(.*) 范式的，则说明是需要进行加解密支持的

#### 密钥

settings.toml 中的 secret_key， 内部代码封装是，会自动生成 encode_secret_key, 本应用内用户无需关心 encode_secret_key。 但若是跨应用使用，则给对方 encode_secret_key

**切记：字符串用 单引号 包围**

#### encode_secret_key 生成命令

```bash
cd src/myproject/common
python crypto.py -a generate -d 'YOUR_SECRET_KEY'
```

#### 加密命令

```bash
cd src/myproject/common
python crypto.py -a encrypt -d 'YOUR_NEED_ENCRYPT_DATA' -k 'YOUR_SECRET_KEY'

```

#### 解密命令

```bash
cd src/myproject/common
python crypto.py -a decrypt -d 'YOUR_ENCRYPTED_DATA' -k 'YOUR_SECRET_KEY'
```

### 数据库初始化（alembic）

1. alembic.ini 中，配置 sqlalchemy 的连接串
2. alembic/env.py 中，添加target_metadata

初始化命令：

```bash
# 切换到和 alembic.ini 同一级的目录
cd src/myproject

# 生成变化
alembic revision --autogenerate -m "init db"

# 执行变更
alembic upgrade head

# 降级
alembic downgrade XXXX
```