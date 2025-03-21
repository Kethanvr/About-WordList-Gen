# Enhanced Smart Wordlist Generator

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![License](https://img.shields.io/badge/license-Educational%20Only-red.svg)

## 🔐 Overview

A sophisticated penetration testing tool that intelligently generates targeted wordlists for security assessments. The generator creates highly effective password combinations by analyzing target information and applying service-specific patterns, dramatically increasing the success rate of authorized security testing.

> ⚠️ **IMPORTANT**: This tool is designed EXCLUSIVELY for legitimate security testing with proper authorization. Any other use may violate applicable laws.

## ✨ Key Features

### 🎯 Smart Targeting
- **Service-Specific Customization**: Optimized wordlists for multiple services:
  - SSH, Web, FTP, Router
  - RDP, SMB, MySQL, PostgreSQL
- **Contextual Password Generation**: Creates logical password combinations based on collected information
- **Dynamic Question Flow**: Adapts questions based on service type

### 🧠 Advanced Generation Capabilities
- **Multi-level Complexity**: Choose from basic, medium, or advanced generation algorithms
- **Intelligent Permutations**: Combines personal data with common password patterns
- **Special Character Variations**: Automatically applies substitutions and variations
- **Leet Speak Transformations**: Converts letters to their numeric/symbolic equivalents

### 🛠️ Professional Tools
- **Password Policy Filters**: Control minimum/maximum length and character requirements
- **Wordlist Analysis**: Get detailed statistics about your generated wordlist
- **Attack Command Suggestions**: Automatically generates ready-to-use commands for Hydra and Medusa
- **Progress Tracking**: Visual feedback during generation and processing
- **Flexible Input Methods**: Both interactive and command-line modes available

### 📊 User Experience
- **Clean CLI Interface**: Color-coded, intuitive command-line interface
- **Sample Password Preview**: Inspect generated passwords before use
- **Robust Error Handling**: Graceful handling of unexpected scenarios

## 🖥️ Usage Examples

### Interactive Mode
```bash
python wordlist_generator.py
```

### Command-Line Mode
```bash
python wordlist_generator.py --service ssh --ip 192.168.1.10 --username admin --firstname john --lastname smith --company acme --complexity 2 --output wordlists/target_ssh.txt
```

## 📋 Command Line Arguments

| Argument | Description |
|----------|-------------|
| `--service` | Target service type (ssh, web, ftp, etc.) |
| `--ip` | Target IP address |
| `--username` | Known username |
| `--firstname` | Target's first name |
| `--lastname` | Target's last name |
| `--company` | Target's company name |
| `--year` | Target's birth year |
| `--complexity` | Password complexity level (1-3) |
| `--output` | Custom output file path |
| `--min-length` | Minimum password length |
| `--max-length` | Maximum password length |

## 🔍 Example Output

```
📊 Wordlist Analysis:
• Total passwords: 1243
• Average length: 9.7 characters
• Length range: 8 to 20 characters
• Passwords with special chars: 537 (43.2%)
• Passwords with digits: 864 (69.5%)
• Passwords with uppercase: 321 (25.8%)
• Common passwords included: 16

Suggested attack commands:
1. hydra -l admin -P results/ssh_20240321_123045_wordlist.txt -s 22 192.168.1.10 ssh
2. medusa -h 192.168.1.10 -u admin -P results/ssh_20240321_123045_wordlist.txt -M ssh -n 22
```

## ⚖️ Legal and Ethical Use

This tool is provided for **educational purposes only**. Users are responsible for:

1. Obtaining explicit written permission before testing any system
2. Following all applicable laws and regulations
3. Adhering to ethical hacking principles
4. Using this tool only on systems they own or are authorized to test

## 🤝 Contributing

Contributions are welcome for improvements that enhance the tool's effectiveness while maintaining its ethical use case. Please follow secure coding practices in all contributions.

---

Created by **Kethan VR** | Enhanced by the security research community