



# def test_ping(client):
#     start_time = time.time()
#     ping_response = client.ping()
#     end_time = time.time()
#     ping_time = (end_time - start_time) * 1000
#
#     ping_res=f'Ping: {ping_time:.2f}ms'
#
#     start_time1 = time.time()
#     server_time = client.time()
#     end_time1 = time.time()
#     request_time1 = (end_time1 - start_time1) * 1000
#
#     request_server_res = f'Request time: {request_time1:.2f}ms'
#
#
#     start_time2 = time.time()
#     ticker = client.ticker_price(symbol='BTCUSDT')
#     end_time2 = time.time()
#     request_time2 = (end_time2 - start_time2) * 1000
#
#     request_ticker_res = f'Request time: {request_time2:.2f}ms'
#
#
#     return ping_res, request_server_res, request_ticker_res
