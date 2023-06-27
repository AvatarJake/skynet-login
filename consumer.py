# import json, os, django
# from confluent_kafka import Consumer


# os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")
# django.setup()
# from rest_framework.exceptions import ValidationError
# # from django.apps import apps

# # Cliente = apps.get_model('clientes','Cliente')

# consumer = Consumer({
#     'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVER'),
#     'security.protocol': os.environ.get('KAFKA_SECURITY_PROTOCOL'),
#     'sasl.username': os.environ.get('KAFKA_USERNAME'),
#     'sasl.password': os.environ.get('KAFKA_PASSWORD'),
#     'sasl.mechanism': 'PLAIN',
#     'group.id': os.environ.get('KAFKA_GROUP'),
#     'auto.offset.reset': 'earliest'
#     })

# consumer.subscribe([os.environ.get('KAFKA_TOPIC')])

# while True:
#     msg=consumer.poll(1.0)

#     if msg is None:
#         continue

#     if msg.error():
#         print("Consumer error: {}".format(msg.error()))
#         continue

#     if msg is not None and not msg.error():
        
#         topic = msg.topic()
#         value = msg.value()
#         data = json.loads(value)
#         print(f"Got this message with Topic: {topic} and value:{value}, with data: {data}")

#         # print("Message Topic: {}".format(msg.topic()))
#         # print("Consumer Key: {}".format(msg.key()))

#         # if topic == os.environ.get('KAFKA_TOPIC'):
#         #     if msg.key()== b'create_user':
#         #         try:
#         #             print(f"User created successfully{data['userID']}")
#         #         except ValidationError as e:
#         #             print(f"Failed to created user{data['userID']}:{str(e)}")
#             #     user_date =json.loads(value)

#             #     user_id=user_data['id']

#             #     cliente, created = Cliente.objects.get_or_create(user_id=user_id,defaults={'Cliente': 0})
#             #     if created:
#             #         cliente.save()
#             # pass
# consumer.close()


