🐕 AI Security Patrol Robot

Unitree Go2 기반 자율주행 경비 로봇 시스템

3D SLAM · ROS2 Nav2 · Grounding DINO · Web Dashboard 기반 통합 관제 플랫폼

📌 Overview

AI Security Patrol Robot은 Unitree Go2 사족보행 로봇을 활용한 자율주행 경비 시스템입니다.

본 프로젝트는 로봇이 스스로 순찰을 수행하며, 주변 환경을 실시간으로 매핑하고, 침입자 또는 위험 상황을 탐지하여 웹 기반 대시보드를 통해 운영자에게 알림을 제공하는 것을 목표로 합니다.

주요 기능
실시간 통합 관제 대시보드
3D SLAM 기반 환경 매핑
ROS2 Nav2 자율주행
Grounding DINO 기반 Zero-shot 객체 탐지
실시간 이벤트 알림
비상정지 및 자동 복귀 기능
🎥 Demo
Dashboard
<img width="1112" height="415" alt="image" src="https://github.com/user-attachments/assets/db317617-4850-46ab-9a1e-c50267b39653" />

SLAM Mapping
<img width="1118" height="392" alt="image" src="https://github.com/user-attachments/assets/0c2bd2ce-769e-45ab-8104-8f3b0479461e" />

Intruder Detection
<img width="1105" height="404" alt="image" src="https://github.com/user-attachments/assets/92ad94e4-f16a-444c-abd7-4a3d8c80c2f3" />

Patrol Navigation
<img width="1095" height="396" alt="image" src="https://github.com/user-attachments/assets/f5b20097-1be7-484d-8864-f0de3836e689" />

🏗️ System Architecture
                         ┌───────────────┐
                         │ Web Dashboard │
                         └───────┬───────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼

 ┌──────────────┐       ┌────────────────┐      ┌──────────────┐
 │ SLAM Module  │       │ Detection AI   │      │ Navigation   │
 └──────┬───────┘       └──────┬─────────┘      └──────┬───────┘
        │                      │                       │
        ▼                      ▼                       ▼

    LiDAR + IMU           Camera Stream           ROS2 Nav2

                               ▼
                        Grounding DINO

                               ▼
                         Alert System
🔄 Workflow
Environment Mapping
        ↓
Map Generation
        ↓
Dashboard Registration
        ↓
Waypoint Selection
        ↓
Autonomous Patrol
        ↓
Object Detection
        ↓
Alert Notification
🚀 Features
1. Web Dashboard

실시간 로봇 상태를 웹 브라우저에서 모니터링할 수 있습니다.

제공 기능
Robot Status
Battery Monitoring
Sensor Monitoring
Live Location Tracking
Alert Notification
Emergency Stop
Return Home
2. 3D SLAM Mapping

FAST-LIO2 기반 환경 매핑 시스템

Features
LiDAR + IMU Fusion
Real-time Mapping
Point Cloud Generation
Occupancy Grid Map Generation
3. Zero-shot Intruder Detection

Grounding DINO를 이용한 텍스트 기반 객체 탐지

Example Prompts
person

intruder

unauthorized person

vehicle

fire extinguisher
Detection Pipeline
Camera Input
      ↓
YOLOv8
      ↓
Grounding DINO
      ↓
Bounding Box
      ↓
Dashboard Alert
4. Autonomous Navigation

ROS2 Nav2 기반 자율주행

Features
Waypoint Navigation
Obstacle Avoidance
Automatic Return
Path Planning
🛠️ Tech Stack
Robot Platform
Unitree Go2
AI
Grounding DINO
YOLOv8
OpenCV
PyTorch
Robotics
ROS2 Humble
Nav2
FAST-LIO2
Backend
FastAPI
Python
Frontend
React
TypeScript
Tailwind CSS
Infrastructure
Docker
Docker Compose
Tailscale
GitHub Actions
📂 Project Structure
AI-Security-Robot
│
├── dashboard
│   ├── frontend
│   └── backend
│
├── slam
│   ├── fastlio2
│   └── mapping
│
├── navigation
│   ├── nav2
│   └── waypoint_manager
│
├── detection
│   ├── yolo
│   ├── grounding_dino
│   └── alert_system
│
├── docker
│
├── docs
│
└── README.md
📊 Performance
Item	Result
SLAM Mapping	✅
Dashboard Monitoring	✅
Object Detection	✅
Alert System	✅
Waypoint Navigation	✅
Autonomous Patrol	✅
Emergency Stop	✅
📋 Use Case
Security Patrol
Patrol Start
      ↓
Area Monitoring
      ↓
Intruder Detected
      ↓
Alert Generation
      ↓
Operator Response
Warehouse Monitoring
Patrol
      ↓
Inventory Area Check
      ↓
Unauthorized Access Detection
      ↓
Alert
👨‍💻 Team Doritos
Name	Role
김인규	AI Detection / Integration
신민서	Dashboard Frontend
신정현	SLAM / Navigation
이가은	Backend / DevOps
🎯 Future Work
Thermal Camera Integration
Gas Leakage Detection
Multi-Robot Coordination
Cloud-Based Monitoring
AI Behavior Analysis
Mobile Application
📚 References
Papers
Grounding DINO (Liu et al., 2023)
FAST-LIO2 (Xu et al., 2022)
LIO-SAM (Shan et al., 2020)
Frameworks
ROS2 Humble
Nav2
PyTorch
FastAPI
