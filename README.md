# Lowfound-Developer-Assessment-SSA
Assesment for Lowfound comapny


You need to create .env file in your project root with this fields:
```
api-key =  <openapi-key>
SECRET_KEY = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```
You can get OpenAI API key following this [instruction](https://help.socialintents.com/article/188-how-to-find-your-openai-api-key-for-chatgpt)
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
