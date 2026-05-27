## Нагрузочное тестирование

### Выводы утилиты ad

#### 1. Статика напрямую через Nginx
root@a66c435065fd:/app# ab -n 1000 -c 10 http://nginx/sample.html
This is ApacheBench, Version 2.3 <$Revision: 1923142 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/
Benchmarking nginx (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests
Server Software:        nginx/1.31.1
Server Hostname:        nginx
Server Port:            80
Document Path:          /sample.html
Document Length:        250974 bytes
Concurrency Level:      10
Time taken for tests:   1.578 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      251284000 bytes
HTML transferred:       250974000 bytes
Requests per second:    633.79 [#/sec] (mean)
Time per request:       15.778 [ms] (mean)
Time per request:       1.578 [ms] (mean, across all concurrent requests)
Transfer rate:          155529.75 [Kbytes/sec] received
Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    0   0.3      0       4
Processing:     4   15   5.7     14      78
Waiting:        1   11   5.0     10      72
Total:          5   16   5.7     15      78
Percentage of the requests served within a certain time (ms)
50%     15
66%     16
75%     17
80%     18
90%     20
95%     24
98%     30
99%     39
100%     78 (longest request)

#### 2. Статика напрямую через Gunicorn
root@a66c435065fd:/app# ab -n 1000 -c 10 http://127.0.0.1:8080/static/sample.html
This is ApacheBench, Version 2.3 <$Revision: 1923142 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/
Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8080
Document Path:          /static/sample.html
Document Length:        151169 bytes
Concurrency Level:      10
Time taken for tests:   60.278 seconds
Complete requests:      1000
Failed requests:        843
(Connect: 0, Receive: 0, Length: 843, Exceptions: 0)
Non-2xx responses:      1000
Total transferred:      151821859 bytes
HTML transferred:       151167680 bytes
Requests per second:    16.59 [#/sec] (mean)
Time per request:       602.781 [ms] (mean)
Time per request:       60.278 [ms] (mean, across all concurrent requests)
Transfer rate:          2459.66 [Kbytes/sec] received
Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       1
Processing:   119  598  64.6    579     836
Waiting:      119  598  64.6    579     835
Total:        120  598  64.6    580     836
Percentage of the requests served within a certain time (ms)
50%    580
66%    592
75%    610
80%    620
90%    707
95%    734
98%    757
99%    784
100%    836 (longest request)

#### 3. Динамика напрямую через Gunicorn
root@a66c435065fd:/app# ab -n 1000 -c 10 http://127.0.0.1:8080/login/
This is ApacheBench, Version 2.3 <$Revision: 1923142 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/
Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8080
Document Path:          /login/
Document Length:        146142 bytes
Concurrency Level:      10
Time taken for tests:   80.355 seconds
Complete requests:      1000
Failed requests:        739
(Connect: 0, Receive: 0, Length: 739, Exceptions: 0)
Total transferred:      146954495 bytes
HTML transferred:       146141164 bytes
Requests per second:    12.44 [#/sec] (mean)
Time per request:       803.551 [ms] (mean)
Time per request:       80.355 [ms] (mean, across all concurrent requests)
Transfer rate:          1785.95 [Kbytes/sec] received
Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       2
Processing:   136  798 526.0    661    5234
Waiting:      136  798 525.7    661    5234
Total:        137  799 526.0    662    5234
Percentage of the requests served within a certain time (ms)
50%    662
66%    760
75%    782
80%    791
90%    854
95%   1124
98%   3141
99%   3637
100%   5234 (longest request)

#### 4. Динамика через Nginx без кэша
root@a66c435065fd:/app# ab -n 1000 -c 10 http://nginx/login/
This is ApacheBench, Version 2.3 <$Revision: 1923142 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/
Benchmarking nginx (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests
Server Software:        nginx/1.31.1
Server Hostname:        nginx
Server Port:            80
Document Path:          /login/
Document Length:        10742 bytes
Concurrency Level:      10
Time taken for tests:   6.729 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      11178000 bytes
HTML transferred:       10742000 bytes
Requests per second:    148.62 [#/sec] (mean)
Time per request:       67.288 [ms] (mean)
Time per request:       6.729 [ms] (mean, across all concurrent requests)
Transfer rate:          1622.29 [Kbytes/sec] received
Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    0   1.9      0      50
Processing:    11   64  84.3     42     654
Waiting:       11   64  84.1     41     654
Total:         12   65  84.9     42     655
Percentage of the requests served within a certain time (ms)
50%     42
66%     48
75%     56
80%     64
90%     76
95%    153
98%    494
99%    543
100%    655 (longest request)

#### 5. Динамика через Nginx с кэшом (proxy_cache) 
root@a66c435065fd:/app# ab -n 1000 -c 10 http://nginx/login/
This is ApacheBench, Version 2.3 <$Revision: 1923142 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/
Benchmarking nginx (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests
Server Software:        nginx/1.31.1
Server Hostname:        nginx
Server Port:            80
Document Path:          /login/
Document Length:        10742 bytes
Concurrency Level:      10
Time taken for tests:   4.099 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      11178000 bytes
HTML transferred:       10742000 bytes
Requests per second:    243.95 [#/sec] (mean)
Time per request:       40.992 [ms] (mean)
Time per request:       4.099 [ms] (mean, across all concurrent requests)
Transfer rate:          2662.99 [Kbytes/sec] received
Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       2
Processing:    11   40   7.0     39      82
Waiting:       11   40   7.0     38      81
Total:         12   41   7.0     39      82
Percentage of the requests served within a certain time (ms)
50%     39
66%     41
75%     42
80%     44
90%     48
95%     55
98%     64
99%     72
100%     82 (longest request)

### Ответы на вопросы:

#### Насколько быстрее отдается статика по сравнению с WSGI?

Статика через Nginx (633 RPS) отдается в 51 раз быстрее, чем динамика через WSGI/Gunicorn (12.4 RPS).

#### Во сколько раз ускоряет работу proxy_cache?

Использование proxy_cache позволило увеличить производительность динамической страницы с 148 RPS (простое проксирование) до 244 RPS (отдача из кэша), что дает ускорение в 1.6 раза на уровне прокси-сервера. Если же сравнивать с прямым обращением к Gunicorn (12 RPS), то связка Nginx+Cache ускоряет ответ в 20 раз.
Примечание: Разница не достигла показателей статики (600 RPS) из-за наличия заголовков 