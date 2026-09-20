import os
from flask import Flask, jsonify
from config import Config, BASE_DIR
from extensions import db, jwt, cors


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}}, supports_credentials=True)

    from routes.auth import auth_bp
    from routes.students import students_bp
    from routes.faculty import faculty_bp
    from routes.academics import academics_bp
    from routes.attendance import attendance_bp
    from routes.marks import marks_bp
    from routes.misc import misc_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(students_bp, url_prefix="/api")
    app.register_blueprint(faculty_bp, url_prefix="/api")
    app.register_blueprint(academics_bp, url_prefix="/api")
    app.register_blueprint(attendance_bp, url_prefix="/api")
    app.register_blueprint(marks_bp, url_prefix="/api")
    app.register_blueprint(misc_bp, url_prefix="/api")

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "message": "Nova Tech University API is running"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"message": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
