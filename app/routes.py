from flask import Blueprint, render_template, Response, request, abort, make_response

from app.captures.capture_b import select_capture_part_b
from app.captures.capture import select_capture
from app.captures.captureFiltersMask import get_esp32_filtered_photo, get_local_filtered_photo
import app.data.data as config_data

main_bp = Blueprint("main",__name__)

# Html
@main_bp.route('/', endpoint='index')
def index():
    return render_template('index.html')

@main_bp.route('/part1_b')
def part1_b():
    return render_template('part1_b.html')


@main_bp.route('/operations',)
def operations():
    return render_template('operations.html')

# Video streaming
@main_bp.route('/video_stream')
def video_stream():
    return Response(select_capture(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
@main_bp.route('/video_stream_b')
def video_stream_b():
    return Response(select_capture_part_b(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
# Fotos
@main_bp.route('/photo_local_filters_mask')
def picture_local():
    image_bytes = get_local_filtered_photo()
    response = make_response(image_bytes)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@main_bp.route('/photo_esp_filters_mask')
def picture_esp():
    image_bytes = get_esp32_filtered_photo()
    response = make_response(image_bytes)
    response.headers.set('Content-Type', 'image/jpeg')
    return response


# HTTP
@main_bp.route('/save-noise',  methods=['POST'])
def save_noise():
    data = request.get_json()   
    
    newMedia = data.get('media')
    newDeviation = data.get('deviation')
    newVariance = data.get('variance')    
    
    print(f"newMedia: {newMedia}, newDeviation: {newDeviation}, newVariance: {newVariance}")
    try:    
        if(newMedia != None):
            newMedia = float(newMedia)   
            if(newMedia < 0): abort(400, "valores no validos, solo numeros")
            
        if(newDeviation != None):
            newDeviation= float(newDeviation)
            if(newDeviation < 0): abort(400, "valores no validos, solo numeros")
            
        if(newVariance != None):
            newVariance = float(newVariance)
            if(newVariance < 0): abort(400, "valores no validos, solo numeros")
        
    except:
        abort(400, "valores no validos, solo numeros")
        pass
        
    config_data.media = newMedia
    config_data.deviation = newDeviation
    config_data.variance = newVariance
    
    return "Se guardaron los parametros de ruido", 200