# Lowfound-Developer-Assessment-SSA
Assesment for Lowfound comapny


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

Create a virtual environment:

```
python3 -m venv venv
```

* If you use Linux/macOS

    ```
    source venv/bin/activate
    ```

* if you use windows

    ```
    source venv/scripts/activate
    ```


Install requirements from  requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Launch backend
```
uvicorn main:app --reload
```
