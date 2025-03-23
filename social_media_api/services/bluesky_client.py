from atproto import Client

client = Client()
profile = client.login("jvpcms.bsky.social", "qc5n-oiop-lz5d-wxbf")
post = client.send_post("Hello world! I posted this via the Python SDK.")
print(post)
