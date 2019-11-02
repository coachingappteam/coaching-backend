from flask import jsonify
from src.DAO.PlanDAO import PlanDAO
from src.DAO.SecurityDAO import SecurityDAO

dao = PlanDAO()
securityDAO = SecurityDAO()