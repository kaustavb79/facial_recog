import base64
import json
import requests
import cv2

def get_face_recognition_response(request, file):
    final_response_json = {
        "status": "failure",
        "is_valid": False,
        "message": "Invalid Data!!!",
        "image": ""
    }
    url = request.api_url + "/api/detect_face/"
    # print(file)
    # print(url)
    header = {
        "accept": "application/json;"
    }
    payload = {'csrfmiddlewaretoken': ""}
    try:
        r = requests.post(url, headers=header, data=payload, files={'input_data': open(file, 'rb')})
    except Exception as e:
        final_response_json['message'] = "failed!!!"
        print(e)
    else:
        if r.status_code == 200:
            data = r.json()
            print("\ndata:",data['data'])
            if bool(data['is_valid']):
                img = cv2.imread(file)
                if data['data']:
                    color = (255, 0, 0)  
                    # Line thickness of 2 px
                    thickness = 2                    
                    # Using cv2.rectangle() method
                    # Draw a rectangle with blue line borders of thickness of 2 px
                    for x in data['data']:
                        img = cv2.rectangle(img, (x['coordinates']['x_min'],x['coordinates']['y_min']), (x['coordinates']['x_max'],x['coordinates']['y_max']), color, thickness)
                        img = cv2.rectangle(img, (x['coordinates']['x_min'],x['coordinates']['y_max']-35), (x['coordinates']['x_max'],x['coordinates']['y_max']), color, thickness)
                        img = cv2.putText(img,x['class'], (x['coordinates']['x_min']+6,x['coordinates']['y_max']-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                        retval, buffer = cv2.imencode('.jpg', img)
                        jpg_as_text = base64.b64encode(buffer)
                        final_response_json['image'] = jpg_as_text.decode('utf-8')
                    final_response_json['status'] = data['status']
                    final_response_json['is_valid'] = data['is_valid']
                    final_response_json['message'] = data['message']
        else:
            final_response_json['message'] = f"STATUS CODE: {r.status_code} --- Message: {r.reason}"
    return final_response_json
