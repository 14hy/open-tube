from app import app

if __name__ == "__main__":
    # context = ('/root/https_keys/certificate.crt', '/root/https_keys/private.key')
    app.run(host="0.0.0.0", port=8888, debug=True)
