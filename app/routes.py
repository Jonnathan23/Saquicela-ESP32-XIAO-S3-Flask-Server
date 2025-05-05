from flask import Blueprint, render_template, Response

from .capture_b import select_capture_part_b
from .capture import select_capture

main_bp = Blueprint("main",__name__)

@main_bp.route('/', endpoint='index')
def index():
    return render_template('index.html')

@main_bp.route('/part1_b')
def part1_b():
    return render_template('part1_b.html')


@main_bp.route('/operations',)
def operations():
    return render_template('operations.html')


@main_bp.route('/video_stream')
def video_stream():
    return Response(select_capture(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
@main_bp.route('/video_stream_b')
def video_stream_b():
    return Response(select_capture_part_b(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')