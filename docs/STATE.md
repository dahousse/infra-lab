# STATE — infra-lab

## 🧭 Version active
main (stable)

## 🧠 AI CLI
tools/ai-cli-v2

Status:
- Router: v2.5 (intent-based)
- Planner: active
- Dispatcher: active
- Async worker: basic (non blocking minimal)
- Engines:
  - vm (Proxmox ready)
  - ollama (fallback chat)
  - terraform (stub)
  - proxmox (stub)

## ⚙️ Infra
infra-lab root:

- ansible/ → automation infra
- terraform/ → infrastructure as code
- tools/ → AI CLI + utilities
- docs/ → knowledge base

## 🔁 Flow system
CLI → Router → Intent → Planner → Dispatcher → Engine

## 🧱 State global
- Git: clean
- Main: stable
- Releases: v2.5 frozen
- Feature branches: archived or merged

## 📌 Notes
- System is functional (not broken)
- Focus is now clarity > complexity
- Next evolution only after stabilization
