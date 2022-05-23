# mini_wallet
Mini Wallet Exercise

## Installation

Clone the code and run install python requirement first

```bash
git checkout master
```

```bash
pip3 install -r requirements.tx
```

## Run env
``` bash
source mini_wallet_env/bin/activate
```

## Run Apps
```
python3 manage.py runserver
```

## Credential for testing user authentication using postman to get token

```bash

http://localhost:8000/api/v1/init

{
	"username" : "testuser",
	"password" : "password"
}
```

## Set Token on Header Postman

```
Authorization token *********
```

## URL

```bash
http://localhost:8000/api/v1/init
http://localhost:8000/api/v1/wallet
http://localhost:8000/api/v1/deposits
http://localhost:8000/api/v1/withdrawals
```
