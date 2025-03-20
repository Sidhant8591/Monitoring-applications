import psutil
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def monitor_metrics():
    cpu_utilization = psutil.cpu_percent()
    mem_utilization = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_traffic = psutil.net_io_counters()
    num_processes = len(psutil.pids())
    
    return cpu_utilization, mem_utilization, disk_usage, network_traffic, num_processes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/metrics")
def metrics():
    cpu_utilization, mem_utilization, disk_usage, network_traffic, num_processes = monitor_metrics()
    
    cpu_gauge = {
        "type": "indicator",
        "mode": "gauge+number",
        "value": cpu_utilization,
        "gauge": {
            "axis": {"range": [None, 100]},
            "bar": {"color": "#1f77b4"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#ccc",
            "steps": [
                {"range": [0, 50], "color": "#d9f0a3"},
                {"range": [50, 85], "color": "#ffeb84"},
                {"range": [85, 100], "color": "#ff5f5f"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": cpu_utilization
            }
        }
    }
    
    mem_gauge = {
        "type": "indicator",
        "mode": "gauge+number",
        "value": mem_utilization,
        "gauge": {
            "axis": {"range": [None, 100]},
            "bar": {"color": "#1f77b4"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#ccc",
            "steps": [
                {"range": [0, 50], "color": "#d9f0a3"},
                {"range": [50, 85], "color": "#ffeb84"},
                {"range": [85, 100], "color": "#ff5f5f"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": mem_utilization
            }
        }
    }
    
    disk_gauge = {
        "type": "indicator",
        "mode": "gauge+number",
        "value": disk_usage,
        "gauge": {
            "axis": {"range": [None, 100]},
            "bar": {"color": "#1f77b4"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#ccc",
            "steps": [
                {"range": [0, 50], "color": "#d9f0a3"},
                {"range": [50, 85], "color": "#ffeb84"},
                {"range": [85, 100], "color": "#ff5f5f"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": disk_usage
            }
        }
    }
    
    network_gauge = {
        "type": "indicator",
        "mode": "gauge+number",
        "value": network_traffic.bytes_sent + network_traffic.bytes_recv,
        "gauge": {
            "axis": {"range": [0, max(network_traffic)]},
            "bar": {"color": "#1f77b4"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#ccc",
            "steps": [
                {"range": [0, max(network_traffic)/2], "color": "#d9f0a3"},
                {"range": [max(network_traffic)/2, max(network_traffic)], "color": "#ffeb84"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": network_traffic.bytes_sent + network_traffic.bytes_recv
            }
        }
    }
    
    processes_gauge = {
        "type": "indicator",
        "mode": "number",
        "value": num_processes,
        "number": {
            "valueformat": "f"
        }
    }
    
    cpu_gauge_layout = {"title": "CPU Utilization"}
    mem_gauge_layout = {"title": "Memory Utilization"}
    disk_gauge_layout = {"title": "Disk Usage"}
    network_gauge_layout = {"title": "Network Usage"}
    processes_gauge_layout = {"title": "Number of Processes"}

    return jsonify({
        "cpuGauge": cpu_gauge,
        "cpuGaugeLayout": cpu_gauge_layout,
        "memGauge": mem_gauge,
        "memGaugeLayout": mem_gauge_layout,
        "diskGauge": disk_gauge,
        "diskGaugeLayout": disk_gauge_layout,
        "networkGauge": network_gauge,
        "networkGaugeLayout": network_gauge_layout,
        "processesGauge": processes_gauge,
        "processesGaugeLayout": processes_gauge_layout
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
