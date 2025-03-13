from flask import Flask, render_template, jsonify, request
import psutil
import datetime
import subprocess

app = Flask(__name__)

# --- In-Memory Data Storage ---
family_info = [
    {"name": "John Doe", "relation": "Father", "birthday": "1965-05-15"},
    {"name": "Jane Doe", "relation": "Mother", "birthday": "1968-08-22"},
    {"name": "Jimmy Doe", "relation": "Son", "birthday": "1995-03-10"},
    {"name": "Jenny Doe", "relation": "Daughter", "birthday": "1998-07-25"},
]

# List of running VMs (each with type, status, vnc_port, and process id)
vms = []
# Base port for VNC (QEMU uses :N which corresponds to port 5900+N)
vnc_base_port = 5901

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/family')
def family():
    return render_template('family.html', family=family_info)

@app.route('/vms')
def vms_page():
    return render_template('vms.html', vms=vms)

@app.route('/personal')
def personal():
    return render_template('personal.html')

@app.route('/stats')
def stats():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()._asdict()
    disk = psutil.disk_usage('/')._asdict()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    battery_obj = psutil.sensors_battery()
    battery_percent = battery_obj.percent if battery_obj else "N/A"

    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_usage = gpus[0].load * 100  # percentage
        else:
            gpu_usage = "N/A"
    except Exception:
        gpu_usage = "N/A"

    return jsonify({
        "cpu": cpu,
        "memory": mem,
        "disk": disk,
        "time": now,
        "battery": battery_percent,
        "gpu": gpu_usage
    })

@app.route('/update_family', methods=['POST'])
def update_family():
    global family_info
    new_data = request.get_json()
    if new_data and "family" in new_data:
        family_info = new_data["family"]
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/create_vm', methods=['POST'])
def create_vm():
    vm_type = request.json.get('type')
    if vm_type not in ['windows', 'linux']:
        return jsonify({"status": "error", "message": "Invalid VM type"}), 400

    # Set image path based on type – adjust these paths accordingly!
    if vm_type == 'windows':
        image_path = 'path/to/windows.img'
    else:
        image_path = 'path/to/linux.img'

    # Allocate a VNC port for this VM
    vnc_port = vnc_base_port + len(vms)
    # QEMU expects the VNC option in the form :N (which maps to port 5900+N)
    vnc_display = vnc_port - 5900

    # Build a basic QEMU command (this is very simplified!)
    command = [
        "qemu-system-x86_64",
        "-m", "2048",
        "-smp", "2",
        "-hda", image_path,
        "-vnc", f":{vnc_display}"
    ]
    try:
        proc = subprocess.Popen(command)
        vm_info = {"type": vm_type, "status": "Running", "vnc_port": vnc_port, "pid": proc.pid}
        vms.append(vm_info)
        return jsonify({"status": "success", "vm": vm_info})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Accessible on your local network (0.0.0.0)
    app.run(host='0.0.0.0', port=3900, debug=True)
