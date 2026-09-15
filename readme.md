# Project Core - NXTGEN '26 Backend Services 🚀

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-009688)](#)

This repository contains the microservice architecture and core API endpoints for our hackathon submission. 

### ⚠️ WARNING ⚠️
**DO NOT DEPLOY THIS TO PRODUCTION.**
Currently bypassing JWT validation for testing purposes. We will fix this before the final pitch.

### Local Setup
1. Clone the repo.
2. Ensure you have a valid `config.json` in the root directory (ask Alex for the keys).
3. Run `pip install -r requirements.txt`
4. Start the ASGI server: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
