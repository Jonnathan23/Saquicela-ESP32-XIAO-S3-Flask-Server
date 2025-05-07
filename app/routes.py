from flask import Blueprint, render_template, Response, request, abort, make_response

from app.captures.capture_b import select_capture_part_b
from app.captures.capture import select_capture, video_capture_esp32, video_capture_local
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
@main_bp.route('/video_stream_local')
def video_stream_local():
    return Response(video_capture_local(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@main_bp.route('/video_stream_esp32')
def video_stream_esp32():    
    return Response(video_capture_esp32(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
@main_bp.route('/video_stream_b')
def video_stream_b():
    return Response(select_capture_part_b(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
# Fotos
@main_bp.route('/photo_local_filters_mask')
def picture_local():   
    return Response(get_local_filtered_photo(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@main_bp.route('/photo_esp_filters_mask')
def picture_esp():    
    return Response(get_esp32_filtered_photo(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# HTTP
@main_bp.route('/set-equalize-option', methods=['POST'])
def setEqualizeOption():
    data = request.get_json() 
    print(data)
    newequalizeOption = data.get('equalizeOption')
    print('newequalizeOption')
    print(newequalizeOption)
    try:           
        if(newequalizeOption == None):
            abort(400, "No ha seleccionado el metodo")            
    except:
        abort(400, "No ha seleccionado el metodo")
        pass        
    
    config_data.operationMask = newequalizeOption
    
    return "OK",200
    


@main_bp.route('/set-operation', methods=['POST'])
def setOperation():
    data = request.get_json() 
    
    newOperationMask = data.get('operations')
    newEqualizeOption = data.get('equalizeOption')
    
    try:           
        if(newOperationMask == None):
            abort(400, "No ha seleccionado el metodo")
            
        if(newEqualizeOption == None):
            abort(400, "No ha seleccionado el metodo")                        
    except:
        abort(400, "No ha seleccionado el metodo")
        pass        
    
    config_data.operationMask = newOperationMask
    config_data.equalizeOption = newEqualizeOption
    
    
    return "OK",200

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

@main_bp.route('/set-mask-values', methods=['POST'])
def setMaskValues():
    data = request.get_json()   
    
    newHeightMask = data.get('maskHeight')
    newWidthMask = data.get('maskWidth')
    newfilterSelected = data.get('filterSelected')   
    newborderSelected = data.get('borderSelected')
    newKernel = data.get('kernelValue')
    
    try:    
        if(newHeightMask != None):
            newHeightMask = int(newHeightMask)   
            if(newHeightMask < 0): abort(400, "valores no validos, solo numeros")
            
        if(newWidthMask != None):
            newWidthMask= int(newWidthMask)
            if(newWidthMask < 0): abort(400, "valores no validos, solo numeros")            
        
        if(newfilterSelected == None or newborderSelected == None):
            abort(400, "valores no validos, solo numeros")
        
        if(newKernel % 2 == 0  ):
            abort(404, 'El kernel no puede ser par')
            
    except:
        abort(400, "valores no validos, solo numeros")
        pass
        
    config_data.heightMask = newHeightMask
    config_data.widthMask = newWidthMask
    config_data.border = newborderSelected
    config_data.filterSelected = newfilterSelected
    config_data.kernel = newKernel
    
    return "Se guardaron los parametros de ruido", 200