from flask import Blueprint, request, jsonify
from models import db, Lead
from utils.auth_middleware import auth_required

leads_bp = Blueprint("leads_bp", __name__)

@leads_bp.route("", methods=["GET", "OPTIONS"])
@auth_required
def get_leads():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    offset = (page - 1) * limit

    total = Lead.query.count()
    leads = Lead.query.order_by(Lead.id.asc()).offset(offset).limit(limit).all()

    lead_data = [
        {"id": l.id, "name": l.name, "email": l.email, "phone": l.phone, "status": l.status}
        for l in leads
    ]

    return jsonify({
        "data": lead_data,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "totalPages": (total + limit - 1) // limit
        }
    })

@leads_bp.route("", methods=["POST", "OPTIONS"])
@auth_required
def add_lead():
    data = request.get_json()
    lead = Lead(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        status=data.get("status")
    )
    db.session.add(lead)
    db.session.commit()
    return jsonify({"message": "Lead added", "lead": {"id": lead.id}})

@leads_bp.route("/<int:id>", methods=["PUT", "OPTIONS"])
@auth_required
def update_lead(id):
    data = request.get_json()
    lead = Lead.query.get(id)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    lead.name = data.get("name", lead.name)
    lead.email = data.get("email", lead.email)
    lead.phone = data.get("phone", lead.phone)
    lead.status = data.get("status", lead.status)
    db.session.commit()
    return jsonify({"message": "Lead updated"})

@leads_bp.route("/<int:id>", methods=["DELETE", "OPTIONS"])
@auth_required
def delete_lead(id):
    lead = Lead.query.get(id)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404
    db.session.delete(lead)
    db.session.commit()
    return jsonify({"message": "Lead deleted"})
