import pika

# RabbitMQ 服务地址和端口
rabbitmq_host = '172.16.8.110'   # 或你的 RabbitMQ 服务器 IP
rabbitmq_port = 5672

# 用户名和密码
username = 'opslte-test'             # 你的用户名
password = 'opslte-test'             # 你的密码

# 创建认证对象
credentials = pika.PlainCredentials(username, password)

# 连接参数
parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host="opslte-test",
    credentials=credentials
)

# 建立连接和通道
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明队列（确保队列存在）
queue_name = 'opslte-test.employee.workflow'
channel.queue_declare(queue=queue_name, durable=True)

# 消费消息的回调函数
def callback(ch, method, properties, body):
    print("Received:", body.decode())
    # 确认消息已处理
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 开始消费
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback
)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
