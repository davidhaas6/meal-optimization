import http.client

conn = http.client.HTTPSConnection("connect.instacart.com")

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer <token>"
    }

conn.request("GET", "/v2/post_checkout/orders/{order_id}/items", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))