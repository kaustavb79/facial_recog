# facial_recog

A General Purpose Face Detection and Facial recognition model training and evaluation api ....

- https://analyticsindiamag.com/face-recognition-system-using-deepfacewith-python-codes/

- https://github.com/serengil/deepface

- Python : 3.8

- Steps to run:
    - pip install -r requirements.txt
    - python manage.py makemigrations & migrate
    - python manage.py runserver
    - python websocket.py ( --- runs on port 8002 , can change it in the file itself and in the _templates/live.html_ file)

- APIS:
    - api/inference/
        - both image and video files
    - api/train/
        - video file
        - your_name

- UI urls:
    - detect/image/ : for live image detection and recognition
    - detect/live/ : for real-time detection and recognition

- RESOURCES:
    - https://drive.google.com/file/d/1KlanVlDiXf9W5MS9gM99G-0JKYYVkxEg/view?usp=sharing