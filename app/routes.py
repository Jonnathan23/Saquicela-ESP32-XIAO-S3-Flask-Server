from flask import Blueprint, render_template, Response
from .capture import select_capture

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/video_stream')
def video_stream():
    return Response(select_capture(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
