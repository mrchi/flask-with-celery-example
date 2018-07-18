# flask-with-celery-example
**请勿用于生产环境**。/ **DO NOT USE THIS IN PRODUCTION APPLICATION.**

这是一个 Demo，介绍一种在 Flask 大型程序结构中使用 Celery 的方式。

欢迎大家测试、提出意见。

## 环境准备/Preparation

推荐版本：

- Python 3.6+；
- Flask 1.0.2；
- Celery 4.2.0；

拉取代码：

```
git clone https://github.com/pallets/flask.git
```

安装依赖（如果你不使用pipenv，可以`pip3 install flask celery redis`）：

```
cd flask-with-celery-example
pipenv install
```

创建环境变量：

```
export FLASK_APP="manage:app"
export FLASK_ENV="development"
```

## 运行/Running

进入项目根目录：

```
cd flask-with-celery-example
```

运行 Flask：

```
flask run
```

运行 Celery：

```
celery worker -A manage:add_app -l info
celery worker -A manage:factorial_app -l info
```

## 测试/Testing

1. 访问 `http://localhost:5000/add` ，该路由中调用了Celery App `add_app` 的任务 `my_add`。结果：Celery app 中输出了运算结果，也输出了 Flask 配置中 `TEST_FOR_APP_CONTEXT` 的值。

```
[config]
.> app:         add_app:0x10ce43828
.> transport:   redis://127.0.0.1:6379/11
.> results:     disabled://
.> concurrency: 4 (prefork)
.> task events: OFF (enable -E to monitor tasks in this worker)

[queues]
.> haha             exchange=haha(direct) key=haha


[tasks]
  . app.celerytasks.add.my_add

[2018-07-18 10:23:27,089: INFO/MainProcess] Connected to redis://127.0.0.1:6379/11
[2018-07-18 10:23:27,098: INFO/MainProcess] mingle: searching for neighbors
[2018-07-18 10:23:28,125: INFO/MainProcess] mingle: all alone
[2018-07-18 10:23:28,136: INFO/MainProcess] celery@InvokerPro.local ready.
[2018-07-18 10:23:59,963: INFO/MainProcess] Received task: app.celerytasks.add.my_add[0796ff5a-49e6-4854-a0e7-d68c332ba3ea]
[2018-07-18 10:23:59,967: WARNING/ForkPoolWorker-2] 1 + 2 = 3
[2018-07-18 10:23:59,969: WARNING/ForkPoolWorker-2] Starbucks
[2018-07-18 10:23:59,971: INFO/ForkPoolWorker-2] Task app.celerytasks.add.my_add[0796ff5a-49e6-4854-a0e7-d68c332ba3ea] succeeded in 0.0048967800000028205s: None
```

2. 访问 `http://localhost:5000/fac` ，该路由中调用了Celery App `factorial_app` 的任务 `my_factorial`。

```
[config]
.> app:         factorial_app:0x10fcda7f0
.> transport:   redis://127.0.0.1:6379/11
.> results:     disabled://
.> concurrency: 4 (prefork)
.> task events: OFF (enable -E to monitor tasks in this worker)

[queues]
.> haha             exchange=haha(direct) key=haha


[tasks]
  . app.celerytasks.factorial.my_factorial

[2018-07-18 10:23:42,053: INFO/MainProcess] Connected to redis://127.0.0.1:6379/11
[2018-07-18 10:23:42,063: INFO/MainProcess] mingle: searching for neighbors
[2018-07-18 10:23:43,089: INFO/MainProcess] mingle: all alone
[2018-07-18 10:23:43,102: INFO/MainProcess] celery@InvokerPro.local ready.
[2018-07-18 10:24:05,689: INFO/MainProcess] Received task: app.celerytasks.factorial.my_factorial[fbce2716-07f0-4c26-be40-5bf278c35fb2]
[2018-07-18 10:24:05,693: WARNING/ForkPoolWorker-2] 10! = 3628800
[2018-07-18 10:24:05,696: INFO/ForkPoolWorker-2] Task app.celerytasks.factorial.my_factorial[fbce2716-07f0-4c26-be40-5bf278c35fb2] succeeded in 0.0036479429999971558s: None
```

## 说明/Explanation

### 诉求

能在 Celery 任务中使用 `current_app` 上下文。

### 实现

- 考虑到 Celery 从 4.0+ 版本开始推荐使用小写配置项，所以不再把 Celery 配置放在 Flask 配置中，而是单独存放；
- Celery 的任务要在 Flask 的上下文中执行，因此要重写 `celeryapp.Task` 类；

### 集成

集成 Celery 到 Flask 中的步骤：

1. 在创建 Celery 任务时创建 Celery App，从配置文件中更新配置；
2. 构建 `init_app(flask_app)` 方法，进行 `celeryapp.Task` 类的重写，并把 Celery app 对象存储到 `flask_app.celery_apps` 属性中。
3. 在 Flask 的 Factory Function 中，调用 `init_app` 方法；
4. 在 Flask 的启动脚本中，从 `flask_app.celery_apps` 属性中取出 Celery app

，绑定到当前模块的全局命名空间 `globals()`；

5. 从 Flask 的启动脚本中启动 Celery app worker；

