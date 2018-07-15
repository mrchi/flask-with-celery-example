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
celery worker -A manage:celery_app --loglevel=info
```

## 测试/Testing

访问 `http://localhost:5000/` ，该路由中调用了Celery的任务 `my_add`。应该能够看到：

1、浏览器响应正常，服务器返回 "Hello, world!”；

2、Celery app 中输出了运算结果，也输出了 Flask 配置中 `TEST_FOR_APP_CONTEXT` 的值。

证明 Celery task正常执行，且是在 Flask 的上下文中执行的。

```
celery@MyLaptop.local v4.2.0 (windowlicker)

Darwin-17.6.0-x86_64-i386-64bit 2018-07-13 21:12:34

[config]
.> app:         app:0x105a476a0
.> transport:   redis://127.0.0.1:6379/0
.> results:     disabled://
.> concurrency: 4 (prefork)
.> task events: OFF (enable -E to monitor tasks in this worker)

[queues]
.> celery           exchange=celery(direct) key=celery


[tasks]
  . app.celerytasks.my_add

[2018-07-13 21:12:35,078: INFO/MainProcess] Connected to redis://127.0.0.1:6379/0
[2018-07-13 21:12:35,087: INFO/MainProcess] mingle: searching for neighbors
[2018-07-13 21:12:36,113: INFO/MainProcess] mingle: all alone
[2018-07-13 21:12:36,123: INFO/MainProcess] celery@InvokerPro.local ready.
[2018-07-13 21:12:43,523: INFO/MainProcess] Received task: app.celerytasks.my_add[b59e1be4-1659-41d4-a9c8-6a3b8c5625b5]
[2018-07-13 21:12:43,536: WARNING/ForkPoolWorker-2] 1 + 2 = 3
[2018-07-13 21:12:43,543: WARNING/ForkPoolWorker-2] Starbucks
[2018-07-13 21:12:43,547: INFO/ForkPoolWorker-2] Task app.celerytasks.my_add[b59e1be4-1659-41d4-a9c8-6a3b8c5625b5] succeeded in 0.01246139400000068s: None
```

## 原理说明

在 Flask 大型程序结构（Factory Mode）中，使用 Celery 有一个困扰：

- Celery task 定义时需要 Celery app 实例；
- Celery app 创建时需要 Flask app 实例，需要获取配置，重写 Task 类已在 Flask 上下文中执行任务；
- Flask app 是在运行时创建的。

以上导致不能使用运行时的 Flask app 创建 Celery 实例和任务。

**本 Demo 参照 Flask 注册 Blueprint 的方式，延迟创建 Celery app 实例，同时在创建 Celery app 实例时，将任务函数修饰为 Celery task，并把 Celery task 绑定到 Flask app上（方便调用）。**

1. 获取任务函数名和任务函数本身的 dict 。
2. 在创建Celery实例时，利用 `@celeryapp.task` 装饰器的特性，修饰任务函数并把新函数绑定到 Flask app上；
3. 在创建 Flask app 的工厂函数中，创建 Celery 实例；
4. 在路由中，使用 `current_app` 应用上下文获得 Celery 任务函数并调用。