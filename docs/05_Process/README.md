# 📋 Processus - Workflow et Procédures

Documentation workflow Git, pre-commit hooks, et setup terminal.

## 📚 Contenu

- **GIT_WORKFLOW.md** - Convention branches et commits
- **PRECOMMIT_SETUP.md** - Pre-commit hooks configuration
- **TERMINAL_SETUP.md** - Shell configuration

## 🔄 Workflow Standard

1. Create branch: git checkout -b feature/mon-feature
2. Develop & test: pytest tests/ -v --cov=src/
3. Commit: git commit -m "feat: description"
4. Push: git push -u origin feature/mon-feature
5. Create PR sur GitHub

Pour **commencer une feature** → [GIT_WORKFLOW.md](./GIT_WORKFLOW.md)

**Voir aussi:** [../](../) - Menu principal
