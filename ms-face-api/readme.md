Project allows to use MS Face API to recognize emotions from images in user's choice directory and save results in csv file.

* face-API-MS-Radboud - prepared specifically for Radboud faces database, containing information about the images

* face-API-MS-universal - can be used for any image

To use this app one have to enter the following information:

```python
subscription_key = 'your-subscription-key'
```

```python
face_api_url = 'your-api-url'
```

```python
filedirectory = 'your/directory'
```

And then run python script. Results will be stored in file *ms_face_api_result_universal.csv* in opened directory.
