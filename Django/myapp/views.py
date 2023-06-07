# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from roboflow import Roboflow
from PIL import Image
from io import BytesIO
import os
import tempfile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .forms import UploadImageForm
from django.shortcuts import redirect


rf = Roboflow(api_key="4rnyXUg1dSwbKKL27upE")
project = rf.workspace("wang-xinjie-luljj").project("toolwear-detection")
model = project.version(1).model


def predict_view(request):
    image_path = os.path.join(os.getcwd(), 'myapp',
                              'static', 'perfecttool.jpg')
    json_output = model.predict(image_path, confidence=70, overlap=30).json()

    # generate the prediction image
    model.predict(image_path, confidence=70, overlap=30).save("prediction.jpg")

    # open the prediction image
    prediction_image = Image.open("prediction.jpg")

    # set the maximum size for the image
    max_size = (500, 500)

    # resize the image while maintaining the aspect ratio
    prediction_image.thumbnail(max_size, Image.ANTIALIAS)

    # get the path to the static files directory
    static_dir = os.path.join(os.getcwd(), "myapp", "static")

    # save the resized image as a PNG file in the static files directory
    dst_file = os.path.join(static_dir, "prediction.png")
    prediction_image.save(dst_file, "PNG")

    # read the PNG file as binary data
    with open(dst_file, "rb") as f:
        img_data = f.read()

    if len(json_output['predictions']) > 0:
        # get the confidence value
        confidence = json_output['predictions'][0]['confidence']
        if confidence is not None:
            percentage = confidence * 100
            accuracy = "{:.2f}%".format(percentage)
        else:
            accuracy = "ACCURACY: N/A"
    else:
        accuracy = "no tool defect."

    # Determine if the stop button should be shown
    if '%' in accuracy:
        show_stop_button = float(accuracy.strip('%')) > 50.0
    else:
        show_stop_button = False

    # render the HTML template with the accuracy value and the prediction image
    return render(request, 'predict.html', {'accuracy': accuracy, 'img_data': img_data, 'show_stop_button': show_stop_button})


def stop_machine(request):
    # do something to stop the machine
    # for example, send the "stop" text to the server
    import socket
    import time

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 5000       # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'stop')
        data = s.recv(1024)

    time.sleep(2)

    return HttpResponse("Machine stopped successfully")


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # Get the path to the static files directory
            static_dir = os.path.join(os.getcwd(), "myapp", "static")

            # Save the image to the desired location
            image_path = os.path.join(static_dir, 'perfecttool.jpg')
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Replace the original image with the new one in the model prediction
            json_output = model.predict(
                'perfecttool.jpg', confidence=70, overlap=30).json()
            model.predict('perfecttool.jpg', confidence=70,
                          overlap=30).save('prediction.jpg')

            return JsonResponse({'status': 'success', 'message': 'Image uploaded and processed successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No image file provided.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def upload_image_and_refresh(request):
    # Call the upload_image function to handle the image upload
    upload_image(request)

    # Redirect to the desired view after successful upload
    return redirect('predict')
