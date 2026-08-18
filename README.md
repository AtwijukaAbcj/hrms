# Solich HRMS

[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL%20v2.1-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Stars](https://img.shields.io/github/stars/solich/solich-hr)](https://github.com/solich/solich-hr/stargazers)
[![Forks](https://img.shields.io/github/forks/solich/solich-hr)](https://github.com/solich/solich-hr/network/members)

> [!IMPORTANT]
> **`2.0` is now this repository’s default branch.** Use it to run or deploy Solich (a plain `git clone` checks it out). To contribute code, branch from and open PRs against `dev/v2.0` — GitHub still pre-selects `2.0` as the PR base, so switch it manually. v1 (`1.0`/`master`) is deprioritized, with fixes considered case-by-case rather than on a guaranteed schedule. Full details → [Discussion #1127](https://github.com/solich/solich-hr/discussions/1127).

> **A comprehensive, free, and open-source Human Resource Management System (HRMS) designed to streamline HR operations and enhance organizational efficiency.**

## 🚀 Features

### Core HR Modules
- 👥 **Employee Management** - Centralized workforce data with LDAP integration
- 🎯 **Recruitment** - End-to-end hiring process from job posting to onboarding
- 📋 **Onboarding & Offboarding** - Structured workflows for employee lifecycle
- ⏰ **Attendance & Time Tracking** - Biometric integration and automated check-in/out
- 🏖️ **Leave Management** - Policy enforcement, approvals, and balance tracking
- 💰 **Payroll** - Automated salary processing, tax calculations, and compliance
- 📊 **Performance Management** - Goal setting, reviews, and continuous feedback
- 🏢 **Asset Management** - Track and manage company resources
- 🎫 **Helpdesk** - Centralized HR support and ticketing system


## 📋 Table of Contents

- [Which Branch Do I Want?](#-which-branch-do-i-want)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Security](#-security)
- [Support](#-support)
- [License](#-license)

## 🌳 Which Branch Do I Want?

- **`2.0`** (default) — the latest stable v2 snapshot. This is what a plain `git clone` gives you. Use it to run or deploy Solich.
- **`dev/v2.0`** — the active integration branch. If you want to contribute code, branch from and open PRs against this, not `2.0`.
- **`1.0`/`master`** — v1, now deprioritized (fixes considered case-by-case, no guaranteed schedule). Not deleted, but no longer where active development happens.

See [Discussion #1127](https://github.com/solich/solich-hr/discussions/1127) for full background on this transition.

## ⚡ Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository (defaults to the stable 2.0 branch)
git clone https://github.com/solich/solich-hr.git
cd solich-hr

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8000
```

### Manual Installation

```bash
# Clone and setup (defaults to the stable 2.0 branch)
git clone https://github.com/solich/solich-hr.git
cd solich-hr

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.dist .env
# Edit .env with your configuration

# Initialize database
python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic

# Run development server
python manage.py runserver
```


## 🛠 Installation

For detailed installation instructions, configuration guides, and platform-specific setup instructions, please visit our comprehensive documentation:

### 📖 [Complete Installation Guide → docs.solich.com/technical/v2.0/ ](https://docs.solich.com/technical/v2.0/)

Our documentation includes:
- **Step-by-step installation** for all supported platforms
- **Database configuration** guides
- **Environment setup** instructions
- **Production deployment** best practices
- **Troubleshooting** common issues
- **Advanced configuration** options

<!-- Need help? Check out the [Installation FAQ](https://docs.solich.com) or reach out to our [community support](#-support). -->

## 🚀 Deployment

For production deployment guides including Nginx, Apache, and cloud platforms:
### 📖 [Deployment Guide → docs.solich.com/technical/v2.0/doc/deployment/nginx-gunicorn](https://docs.solich.com/technical/v2.0/doc/deployment/nginx-gunicorn)


## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone your fork
git clone -b dev/v2.0 https://github.com/YOUR_USERNAME/solich-hr.git
cd solich-hr

# Add upstream remote
git remote add upstream https://github.com/solich/solich-hr.git

# Create feature branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements.txt

# Submit pull request
```

> **Note:** `2.0` is the repo default, so GitHub pre-selects it as your PR base. Before submitting, change the base branch to `dev/v2.0` — that's where active development and reviews happen, not `2.0`.

### Code Standards

- Follow [PEP 8](https://pep8.org/) for Python code
- Use [Black](https://black.readthedocs.io/) for code formatting
- Write tests for new features
- Update documentation for user-facing changes

## 🔒 Security

### Security Features

- 🔐 **Authentication & Authorization** - Role-based access control
- 🛡️ **Data Protection** - Encrypted sensitive data storage
- 🔍 **Audit Trails** - Comprehensive activity logging
- 🚫 **Input Validation** - XSS and injection protection
- 🔒 **Session Security** - Secure session management

### Reporting Security Issues

Please report security vulnerabilities via [GitHub Private Vulnerability Reporting](https://github.com/solich/solich-hr/security/advisories/new), not email. Do not create public GitHub issues for security vulnerabilities. See [SECURITY.md](SECURITY.md) for full details.

### Security Best Practices

- Always use HTTPS in production
- Regularly update dependencies
- Use strong passwords and enable 2FA
- Monitor logs for suspicious activities

## 📞 Support

### Community Support

- 📖 **Documentation**: [docs.solich.com](https://docs.solich.com)
- 💬 **GitHub Discussions**: [GitHub Discussions](https://github.com/solich/solich-hr/discussions)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/solich/solich-hr/issues)
- ✨ **Feature Requests**: [GitHub Issues](https://github.com/solich/solich-hr/issues)

### Professional Support

For enterprise support, custom development, and consulting services:
- 📧 **Email**: support@solich.com
- 🌐 **Website**: [www.solich.com](https://www.solich.com)


## 📄 License

This project is licensed under the [LGPL-2.1 License](LICENSE) - see the LICENSE file for details.

<div align="center">

**Made with ❤️ by the Solich Team**

[⭐ Star us on GitHub](https://github.com/solich/solich-hr) | [🐛 Report Bug](https://github.com/solich/solich-hr/issues) | [💡 Request Feature](https://github.com/solich/solich-hr/issues)

</div>
