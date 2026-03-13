from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route("/trigger-argo", methods=["POST"])
def trigger_argo():

    try:
        subprocess.run([
            "argo",
            "submit",
            "--from",
            "workflowtemplate/pdf-trainer-workflow",
            "-n",
            "argo"
        ], check=True)

        return jsonify({"status": "workflow triggered"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9080)