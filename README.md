# Lowfound-Developer-Assessment-SSA
Assesment for Lowfound comapny

Launch backend locally in ~/lowfound-backend/app
```
uvicorn main:app --reload
```

Launch frontend locally in ~/lowfound-frontend
```
yarn quasar dev
```

You need to have .env file in your project root with this fields:
```
api-key =  <openapi-key>
SECRET_KEY = <password-hash-key>
```
### How to launch frontend

Install [yarn](https://classic.yarnpkg.com/en/docs/install#windows-stable)

Go to /lowfound-frontend

Run those commands: 

```
yarn
```

```
yarn quasar dev
```
### How to launch backend

Go to /lowfound-backend

Install requirements from  requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```


```
pip install -r requirements.txt
```
Launch backend
```
uvicorn main:app --reload
```
